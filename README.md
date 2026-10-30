# Jing Wang · 王靖

基于 [luost26/academic-homepage](https://github.com/luost26/academic-homepage) 视觉样式制作的单页学术主页。保留原模板的 Bootstrap 网格、浅灰背景、左侧简介与白色圆角卡片，并参考 [Yiqian Wu 的主页](https://onethousandwu.com/index.html) 安排学术内容。

免费网址：<https://nnlrl.github.io/>。中文版为 `index.html`，英文版为 `en.html`。

## 维护内容

修改 `data/profile.json`，然后运行：

```sh
python3 scripts/build_site.py
```

生成的 HTML 直接包含完整正文，关闭 JavaScript 也可以阅读。无 Node、Ruby 或数据库依赖；所有样式均随站点本地提供。

## 本地预览

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

打开 <http://127.0.0.1:8765/>。页面支持页内导航、中英文切换、展开合作论文和“打印 / 保存 PDF”。

## GitHub Pages

将站点文件推送到 `nnlrl/nnlrl.github.io` 的发布分支。在仓库 Settings → Pages 中，将发布来源设为该分支的根目录。`.nojekyll` 让 GitHub Pages 直接发布静态文件，不需要安装 Jekyll。

## 内容与边界

- 内容以用户于 2026-10-30 提供的《王靖_高校讲师简历.docx》为准。博士后年份为 **2024–2026**。
- 展示全部 11 篇已发表论文，默认突出 3 篇第一作者论文，其他 8 篇可展开。
- 三篇第一作者论文提供 DOI 链接，其他论文提供明确标注的 PubMed 检索入口。
- 专利保留简历中的名称、发明人和申请号，不依据申请号推断授权状态。英文专利名为内容翻译。
- 不展示未经再次核验的影响因子、期刊分区、引用次数或在审论文。
- 公开页面展示工作邮箱和 GitHub；没有加入出生日期、民族、手机号，也没有上传原始简历文件。
- 没有提供个人照片，因此使用姓名缩写作为标识。
- 页面上的“打印 / 保存 PDF”调用浏览器打印功能，不是下载一个另行制作的 PDF 文件。

## 模板来源与许可

`assets/css/global.css` 来自原模板，保留其卡片和导航基础样式。Bootstrap 4.6.0 的发行样式本地存放在 `assets/vendor/bootstrap.min.css`，保留文件头许可声明。站点适配内容保留原模板 MIT 许可和页脚来源链接。

原模板版权：Copyright (c) 2024 Shitong Luo。详见 `LICENSE`。
