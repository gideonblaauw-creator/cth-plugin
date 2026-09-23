#!/usr/bin/env bash
# workbench-pdf-read — harness PDF keyword search and extract for grants/research.
# Protocol entry point: never invoke raw pdfgrep one-liners; use this script or the skill.
set -euo pipefail

readonly SCRIPT_NAME="workbench-pdf-read"
readonly VERSION="1.0.0"

usage() {
  cat <<'EOF'
Usage: workbench-pdf-read.sh PDF_PATH [PATTERN] [OPTIONS]

Search a PDF with pdfgrep or extract full text with pdftotext.

Arguments:
  PDF_PATH              Path to the PDF (required)
  PATTERN               Extended regex for search mode (optional if --pattern set)

Options:
  --pattern REGEX       Search pattern (alias for positional PATTERN)
  --ignore-case, -i     Case-insensitive search (pdfgrep -i)
  --page-number, -n     Prefix matches with page numbers (pdfgrep default; explicit flag)
  --with-filename, -H   Prefix matches with file name (pdfgrep -H)
  --count, -c           Print match count only (pdfgrep -c)
  --max-count NUM, -m   Stop after NUM matching lines per file
  --perl-regexp, -P     Use PCRE regex (pdfgrep -P)
  --context NUM, -C     Show NUM lines of context (pdftotext + grep fallback; not native pdfgrep)
  --extract PATH        Full-text extract to PATH (pdftotext; ignores PATTERN)
  --quiet, -q           Suppress match lines; exit 0 if any match, 1 if none
  --help, -h            Show this help
  --version, -V         Show version

Examples:
  workbench-pdf-read.sh report.pdf "blended finance"
  workbench-pdf-read.sh report.pdf --pattern "grant" -i -C 2
  workbench-pdf-read.sh report.pdf --extract /tmp/report.txt

See docs/workbench-pdf-reader.md for install and VPS paths.
EOF
}

err() {
  echo "${SCRIPT_NAME}: $*" >&2
  exit 1
}

require_cmd() {
  local cmd="$1"
  local hint="$2"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    err "${cmd} not found. ${hint} See docs/workbench-pdf-reader.md"
  fi
}

validate_pdf() {
  local pdf="$1"
  if [[ ! -f "${pdf}" ]]; then
    err "PDF not found: ${pdf}"
  fi
  if [[ ! -r "${pdf}" ]]; then
    err "PDF not readable: ${pdf}"
  fi
}

print_header() {
  local pdf="$1"
  local pattern="${2:-}"
  local mode="$3"
  echo "=== ${SCRIPT_NAME} v${VERSION} ==="
  echo "file: ${pdf}"
  echo "mode: ${mode}"
  if [[ -n "${pattern}" ]]; then
    echo "pattern: ${pattern}"
  fi
  echo "---"
}

run_extract() {
  local pdf="$1"
  local out="$2"
  require_cmd pdftotext "Install: sudo apt install poppler-utils (Debian/Ubuntu) or brew install poppler (macOS)."
  validate_pdf "${pdf}"
  print_header "${pdf}" "" "extract"
  local out_dir
  out_dir="$(dirname "${out}")"
  if [[ ! -d "${out_dir}" ]]; then
    err "Output directory does not exist: ${out_dir}"
  fi
  if [[ -e "${out}" && ! -w "${out}" ]]; then
    err "Output path not writable: ${out}"
  fi
  pdftotext -layout "${pdf}" "${out}"
  local bytes
  bytes="$(wc -c <"${out}" | tr -d ' ')"
  echo "extracted: ${out} (${bytes} bytes)"
}

run_search_pdfgrep() {
  local pdf="$1"
  local pattern="$2"
  shift 2
  local -a pdfgrep_args=(-n)
  local quiet=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -i|--ignore-case) pdfgrep_args+=(-i) ;;
      -n|--page-number) pdfgrep_args+=(-n) ;;
      -H|--with-filename) pdfgrep_args+=(-H) ;;
      -c|--count) pdfgrep_args+=(-c) ;;
      -P|--perl-regexp) pdfgrep_args+=(-P) ;;
      -q|--quiet) quiet=1; pdfgrep_args+=(-q) ;;
      -m|--max-count)
        [[ $# -ge 2 ]] || err "--max-count requires a number"
        pdfgrep_args+=(-m "$2")
        shift
        ;;
      *)
        err "Unknown option for pdfgrep search: $1"
        ;;
    esac
    shift
  done

  require_cmd pdfgrep "Install: sudo apt install pdfgrep poppler-utils (Debian/Ubuntu) or brew install pdfgrep (macOS)."
  validate_pdf "${pdf}"

  if [[ "${quiet}" -eq 0 && "${pdfgrep_args[*]}" != *"-c"* ]]; then
    print_header "${pdf}" "${pattern}" "search (pdfgrep)"
  fi

  # shellcheck disable=SC2086
  pdfgrep "${pdfgrep_args[@]}" -- "${pattern}" "${pdf}"
}

run_search_context() {
  local pdf="$1"
  local pattern="$2"
  local context="$3"
  shift 3
  local ignore_case=0
  local quiet=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -i|--ignore-case) ignore_case=1 ;;
      -q|--quiet) quiet=1 ;;
      -m|--max-count|-n|--page-number|-H|--with-filename|-c|--count|-P|--perl-regexp)
        echo "${SCRIPT_NAME}: note: $1 ignored in --context mode (pdftotext + grep fallback)" >&2
        [[ "$1" == "-m" || "$1" == "--max-count" ]] && shift
        ;;
      *)
        echo "${SCRIPT_NAME}: note: ignoring unsupported flag in --context mode: $1" >&2
        ;;
    esac
    shift
  done

  require_cmd pdftotext "Install: sudo apt install poppler-utils."
  require_cmd grep "grep is required for --context fallback."
  validate_pdf "${pdf}"

  if [[ "${quiet}" -eq 0 ]]; then
    print_header "${pdf}" "${pattern}" "search (pdftotext + grep -C ${context})"
  fi

  local tmp
  tmp="$(mktemp)"
  pdftotext -layout "${pdf}" "${tmp}"

  local -a grep_args=(-n -E -C "${context}")
  if [[ "${ignore_case}" -eq 1 ]]; then
    grep_args+=(-i)
  fi

  local rc=0
  if ! grep "${grep_args[@]}" -- "${pattern}" "${tmp}"; then
    rc=$?
    if [[ "${rc}" -eq 1 ]]; then
      [[ "${quiet}" -eq 0 ]] && echo "(no matches)"
    fi
  fi
  rm -f "${tmp}"
  exit "${rc}"
}

main() {
  local pdf=""
  local pattern=""
  local extract_out=""
  local context=""
  local -a passthrough=()

  if [[ $# -eq 0 ]]; then
    usage
    exit 0
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)
        usage
        exit 0
        ;;
      -V|--version)
        echo "${SCRIPT_NAME} ${VERSION}"
        exit 0
        ;;
      --extract)
        [[ $# -ge 2 ]] || err "--extract requires an output path"
        extract_out="$2"
        shift 2
        ;;
      --pattern)
        [[ $# -ge 2 ]] || err "--pattern requires a regex"
        pattern="$2"
        shift 2
        ;;
      -C|--context)
        [[ $# -ge 2 ]] || err "--context requires a line count"
        context="$2"
        shift 2
        ;;
      -i|--ignore-case|-n|--page-number|-H|--with-filename|-c|--count|-P|--perl-regexp|-q|--quiet)
        passthrough+=("$1")
        shift
        ;;
      -m|--max-count)
        [[ $# -ge 2 ]] || err "--max-count requires a number"
        passthrough+=("$1" "$2")
        shift 2
        ;;
      --)
        shift
        break
        ;;
      -*)
        err "Unknown option: $1 (try --help)"
        ;;
      *)
        if [[ -z "${pdf}" ]]; then
          pdf="$1"
        elif [[ -z "${pattern}" ]]; then
          pattern="$1"
        else
          err "Unexpected argument: $1"
        fi
        shift
        ;;
    esac
  done

  # Remaining positional args after --
  while [[ $# -gt 0 ]]; do
    if [[ -z "${pdf}" ]]; then
      pdf="$1"
    elif [[ -z "${pattern}" ]]; then
      pattern="$1"
    else
      err "Unexpected argument: $1"
    fi
    shift
  done

  [[ -n "${pdf}" ]] || err "PDF_PATH is required (try --help)"

  if [[ -n "${extract_out}" ]]; then
    if [[ -n "${pattern}" || -n "${context}" ]]; then
      echo "${SCRIPT_NAME}: note: --extract ignores search pattern/context" >&2
    fi
    run_extract "${pdf}" "${extract_out}"
    exit 0
  fi

  [[ -n "${pattern}" ]] || err "PATTERN is required for search mode (or use --extract PATH)"

  if [[ -n "${context}" ]]; then
    run_search_context "${pdf}" "${pattern}" "${context}" "${passthrough[@]}"
  else
    run_search_pdfgrep "${pdf}" "${pattern}" "${passthrough[@]}"
  fi
}

main "$@"
