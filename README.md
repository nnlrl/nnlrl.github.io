# Jing Wang · 王靖

基于 [luost26/academic-homepage](https://github.com/luost26/academic-homepage) 定制的单页学术主页。使用用户选定的孟菲斯风格，奶白底色搭配黄色、珊瑚粉、薄荷绿与几何装饰；顶栏使用带 Home 标记的黄色文件夹。大区块统一左上圆角和右下投影；嵌套小框使用左上与右下圆角、2px 虚线边框，无投影。

免费网址：<https://nnlrl.github.io/>。默认首页 `index.html` 为英文，中文版为 `zh.html`；`en.html` 保留为英文兼容入口。

## 维护内容

修改 `data/profile.json`，然后运行：

```sh
python3 scripts/build_site.py
```

生成的 HTML 直接包含完整正文，关闭 JavaScript 也可以阅读。无 Node、Ruby 或数据库依赖；样式与字体均随站点本地提供。

## 本地预览

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8765/>。页面支持页内导航、中英文切换、展开合作论文和“打印 / 保存 PDF”。手机使用单列布局，打印时展开全部论文。

## GitHub Pages

将站点文件推送到 `nnlrl/nnlrl.github.io` 的发布分支。在仓库 Settings → Pages 中，将发布来源设为该分支的根目录。`.nojekyll` 让 GitHub Pages 直接发布静态文件，不需要安装 Jekyll。

## 内容与边界

- 内容以用户于 2026-10-30 提供的《王靖_高校讲师简历.docx》为准。博士后年份为 **2024–2026**。
- 展示全部 11 篇已发表论文，默认突出 3 篇第一作者论文，其他 8 篇可展开。
- 三篇第一作者论文提供 DOI 链接，其他论文提供明确标注的 PubMed 检索入口。
- 专利保留简历中的名称、发明人和申请号，不依据申请号推断授权状态。英文专利名为内容翻译。
- 不展示未经再次核验的影响因子、期刊分区、引用次数或在审论文。
- 公开页面展示工作邮箱和 GitHub；没有加入出生日期、民族、手机号，也没有上传原始简历文件。
- 没有提供个人照片，因此使用姓名作为标识。
- 页面上的“打印 / 保存 PDF”调用浏览器打印功能，不是下载一个另行制作的 PDF 文件。

## 模板来源与许可

正式页面使用 `assets/css/site-base.css` 和 `assets/css/memphis.css`，不依赖前端框架。黄色文件夹为本站绘制的 SVG，位于 `assets/images/home-folder-yellow.svg`。站点保留原模板 MIT 许可和页脚来源链接。

原模板版权：Copyright (c) 2024 Shitong Luo。详见 `LICENSE`。

## 字体

- 正文：Hanken Grotesk。
- 主标题与论文标题：Bricolage Grotesque。
- 章节标题：Special Elite。
- 导航、日期与辅助标签：IBM Plex Mono。
- 中文字形由系统中文字体补充。

字体在站点本地提供，文件来自此前参考的 [Yiqian Wu 主页](https://onethousandwu.com/index.html) 公开字体目录。字体许可文本随文件保留在 `assets/fonts/`。旧版样式和设计 demo 仍留在本地供参考，正式页面不加载它们。
