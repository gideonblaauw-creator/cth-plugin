/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  ncukSidebar: [
    'index',
    {
      type: 'category',
      label: 'Themes',
      collapsed: false,
      items: ['energy', 'health', 'education'],
    },
  ],
};

module.exports = sidebars;
