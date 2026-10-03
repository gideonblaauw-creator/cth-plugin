# Wire brief — diagram tool (example)

## GOAL
_Meta del pedido en una frase._
Build a Workbench diagram tool that produces a standard wire diagram from each ask.

## ACTORS
_Quién interviene._
- Gideon: requests wire diagrams and confirms strategy output.
- Cloud Hands: implements the tool in the GitHub repo and VPS hooks.
- Workbench: hosts the repeatable diagram workflow.

## STEPS
_Pasos actor-verbo-objeto._
1. Gideon requests a wire diagram from the Workbench tool.
2. Cloud Hands connect the GitHub repo to the diagram tool.
3. Cloud Hands define the standard diagram generation path on the VPS.
4. Cloud Hands convert audio input into STE-80 English text.
5. Cloud Hands convert the STE-80 brief into a wire diagram.

## STATUS
_Estado conocido._
The diagram tool does not exist yet on the Workbench.

## LOCKS
_Acuerdos fijos._
- Use STE-80 controlled English inspired by ASD-STE100 and Karpathy’s Oct 2026 post.
- Hook the cth-plugin GitHub repo to the tool.

## UNKNOWN
_Sin inventar._
- Exact VPS path for diagram generation (source says “check VPS” only).
- Karpathy post URL not spoken in source.

## OUT OF SCOPE
_Excluido._
- Grant or proposal documents.
- Non-diagram social assets.
