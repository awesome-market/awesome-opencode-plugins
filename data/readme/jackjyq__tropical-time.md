<div align="center">

<img src="./src/static/favicon/android-chrome-192x192.png" alt="Tropical Time Icon" width="192">

# Tropical Time ｜ 热带时光

A sensual, tropical-inspired color theme for developers.

专为开发者打造, 富有质感的热带风情主题

</div>

## 🌴 About

The dark themes are designed with enhanced readability to work well with monitors that have reduced brightness, while the light themes maintain a consistent color schema that complements the dark variants. 

Here's how I use the themes:

<details>
<summary> 🏢 Work </summary>

- **System:** Windows 11 dark mode
- **Display:** Monitor with reduced lightness for better eye care
  - `Nightmare` themes for WSL applications
  - `Twilight` themes for Windows native applications
</details>

<details>
<summary> 🏡 Home </summary>

- **System:** macOS light mode
- **Display:** Monitor with normal lightness for better display performance
  - `Daydream` themes for coding
  - `Morninglight` themes for note-taking
</details>

## 🚀 Quick Start

<details>
<summary> syntax highlighting </summary>

- [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=jackjyq.tropical-time)
- [Windows Terminal](./dist/windowsterminal)
- [OpenCode](./dist/opencode/) -> `~/.config/opencode/themes/`
- [Notepad++ Markdown](./dist/npp-markdown/) -> `%AppData%\Notepad++\userDefineLangs`
- [Vim](./dist/vim/) -> `~/.vim/colors/`
- [more...](./dist/)
</details>

<details>
<summary> artworks </summary>

- [Icon](./src/static/favicon/)
- [Wallpaper](./src/static/wallpaper/) -> `for Desktop & Mobile Phone`
- [Wallpaper for E-ink](./src/static/wallpaper-eink/) -> `for Kindle & BOOX`
</details>

## 🎨 Design

<details>
<summary> color palettes </summary>

- [Nightmare & Daydream Palette](https://harmonizer.evilmartians.com/#jZI9b8IwEIb_y3WNqnw5IR4BqQuoqLBUVQcTjIlw7MhxaBHKf6-MCjlnQNjbPXleO3e-wImbttIKaBSA5CcuW6BfF1Cs5kBhQuYQQKmVNay1QCckgPJgdM2Ahq8hKZKchPcV3eCMNY7HfXBPykZJmZcUxUU2yckDPx35qefHD0xCFp5JnjbzkZk_bRYjs_D_Nkm9vvlJqpOy_w7g0HFvFh98BwEwJSQHGofotHfDlOADJBh-cin1zwAnGC6qGnlRhNmb4VwhmGK44UwilmM2OzOFb4rZ-nhGKMFoKjt0lzjDbNWZRmJaYLpkgivLBpx47VlV6ogYCV13W25tpUQL9HKf01LvuAQKrCld2K4yvLSVVq4OFPZio6cCbsP6r9bsFwLYipmW2iwqcbBA4WXP3B7AnJmjq0ex29f69du1ZcYCTdxjkdqsG1a60NaILfT9Hw)
- [Morninglight & Twilight Palette](https://harmonizer.evilmartians.com/#jZJBb8IgFMe_y9u1WWgrtuWoS3bRzEwvZtkBK8VGCg2lbsb0uy-YaV97MHJ8P_4_HjwucBK2KY0GFgagxEmoBtjXBTSvBDBI6QwCyI12ljcOWEoDyA_WVBwYeSU0ixNK7iu8wTmvPY-64G6ajkzTgSmM0jBCpuiBaTIyTQamR0lKt4MkfTqZjJLJ08lslMyG946HF48HJt0q1X0HcGjFYCqfYg8BcC2VABYRdNqH5VqKHlIMt0Ip89PDFMNFWaFcGGL2boXQCE4w3AiuEEswm5-5xp1itj6eEYoxmqkW9RJNMVu1tlaYZpguuRTa8R7Hg-dZlfqIGCX-dRvhXKllA-xyn9PS7IUCBrzOvWxfWpG70mhfBwaF3JiZhNuw_qsV_4UAdnJulLGLUh4cMHgpiiIrwh68cXv0dUJIEUfX-nXv2nHrgPkf4Leta557aWPlDrruDw)
- [E-ink Grey Scale Palette](https://huetone.ardov.me/?palette=N4IgdghgtgpiBcICiBLMBrEAaEALArjAM4IDaoksCIADNiAMYD2ANkwE4nykgDENAwSAC6AXywVocRAEZ6zNpzJ8ZqtSPGSqiAEzzWHLj147TZjRPBTqAZn2KjfG85cWt0kABZ7h5b08BgW5W2iAArD5K3HxhsXHBlB4AbJGOvEkZmQnWiADsqX65RcXZoQAcBdG8ZTW1pR4AnJXGDa1t9dQAgs18EH39HYgAQj28AEYTk4MgAMKjDAuL0wAiowAmG5vTSKMwe-vTAGKjAGZn5xrCOAAuTGDEygDi7DAAnhpAA)

</details>

<details>
<summary> themes </summary>

| Palettes                                                          | Description                         | 描述               |
| ----------------------------------------------------------------- | ----------------------------------- | ------------------ |
| [Tropical Morninglight](./src/palettes/tropical_morninglight.yml) | fresh and golden light theme        | 清亮柔和的淡金主题 |
| [Tropical Daydream](./src/palettes/tropical_daydream.yml)         | graceful and paper-like light theme | 淡雅如纸的白昼主题 |
| [Tropical Twilight](./src/palettes/tropical_twilight.yml)         | ethereal and deep blue dark theme   | 空灵深邃的深蓝主题 |
| [Tropical Nightmare](./src/palettes/tropical_nightmare.yml)       | vibrant and juicy dark theme        | 明艳饱满的暗夜主题 |

</details>

## 🛠️ Develop

[![uv](https://img.shields.io/badge/uv-0.9%2B-purple)](https://docs.astral.sh/uv/)
[![Node.js](https://img.shields.io/badge/node.js-24%2B-green)](https://nodejs.org/en/)
[![just](https://img.shields.io/badge/just-1.34%2B-red)](https://github.com/casey/just)

After install the above dependencies, run `just` to view available recipes.

## 💡 Tips

The theme works best with the following settings:

<details>
<summary>monitor & display</summary>

- enable Eye Care Mode (or Night Shift) feature
- reduce the monitor's lightness
</details>

<details>
<summary>bold text rendering</summary>

disable the bold text rendering feature in your terminal

VSCode Integrated Terminal

```json
{
  "terminal.integrated.drawBoldTextInBrightColors": false,
  "terminal.integrated.fontWeightBold": "normal"
}
```

Windows Terminal

```json
{
  "profiles": {
    "defaults": {
      "intenseTextStyle": "none"
    }
  }
}
```

</details>

<details>
<summary>coding font</summary>

- [MapleMonoNL-NF-CN](https://github.com/subframe7536/maple-font/releases)
- [SarasaTermSC-Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd/releases)

</details>

## 🗺️ Roadmap

<details>
<summary>List of features</summary>

- [x] dark palette
- [x] light palette
- [x] icon
- [x] wallpaper
- [x] VSCode theme
- [x] Vim theme
- [x] Terminal theme
- [x] OpenCode theme
- [x] dark variant palette
- [x] light variant palette
- [ ] zed theme
- [ ] batcat theme

</details>

## 📄 License

this project is licensed under the [MIT License](LICENSE.txt).

## 🙏 Acknowledgements

<details>
<summary>Inspired by and built upon</summary>

- [iTerm2-Color-Schemes](https://github.com/mbadolato/iTerm2-Color-Schemes) - Terminal color scheme collection
- [GitHub VSCode Themes](https://github.com/primer/github-vscode-theme) - GitHub's official VS Code theme
- [Brogrammer Plus](https://github.com/jackjyq/vscode-theme-brogrammer-plus) - Brogrammer theme variant
- [Edditoria](https://github.com/Edditoria/markdown-plus-plus) - Notepad++ markdown syntax highlighting support

</details>
