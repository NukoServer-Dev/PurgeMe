import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PurgeMeドキュメント",
  description: "PurgeMeのドキュメント",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'ホーム', link: '/' },
      { text: '導入する', link: '/docs/invite' },
      { text: 'コマンド一覧', link: '/docs/commands' },
    ],

    sidebar: [
      {
        text: 'ドキュメント',
        items: [
          { text: '導入する', link: '/docs/invite' },
          { text: 'コマンド一覧', link: '/docs/commands' },
          { text: 'コマンドの権限', link: '/docs/permissions' },
          { text: '他Botとの連携', link: '/docs/connection' },
          { text: 'エラーの解説', link: '/docs/errors' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/NukoServer-Dev/PurgeMe' }
    ]
  }
})
