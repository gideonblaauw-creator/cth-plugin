// @ts-check
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'NCUK REIN data room',
  tagline: 'Read-only fallback — placeholders only',
  url: 'https://dataroom.cleantechhub.net',
  baseUrl: '/ncuk/',
  organizationName: 'CleantechHUB',
  projectName: 'ncuk-dataroom-fallback',
  onBrokenLinks: 'throw',
  i18n: { defaultLocale: 'en', locales: ['en'] },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: { defaultMode: 'light', respectPrefersColorScheme: true },
      navbar: {
        title: 'NCUK data room',
        items: [
          { to: '/', label: 'Start', position: 'left' },
          { href: 'https://drive.google.com/drive/folders/1SbHKtgtLRVDmVp4_wofcRDYqZRVpzzO9', label: 'Drive root', position: 'right' },
        ],
      },
      footer: {
        style: 'dark',
        copyright: 'REIN Hubs — placeholder footer. Awaiting Gideon approval.',
      },
    }),
};

module.exports = config;
