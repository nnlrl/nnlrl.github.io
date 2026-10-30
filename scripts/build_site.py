#!/usr/bin/env python3
"""Render the bilingual, dependency-free static homepage from profile.json."""

import html
import json
import re
from pathlib import Path
from string import Template
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def escape(value):
    return html.escape(str(value), quote=True)


def render(profile, lang):
    def text(value):
        return escape(value[lang] if isinstance(value, dict) else value)

    zh = lang == "zh"
    labels = {
        "about": "关于我" if zh else "About",
        "experience": "科研与教育经历" if zh else "Experience & Education",
        "publications": "学术论文" if zh else "Publications",
        "projects": "科研项目" if zh else "Research Projects",
        "patents": "发明专利" if zh else "Patents",
        "skills": "研究与技术能力" if zh else "Research Skills",
        "awards": "荣誉与奖励" if zh else "Honors & Awards",
        "contact": "联系我" if zh else "Contact",
    }

    def section(key, content, extra=""):
        return (
            f'<section class="card border-0 shadow-sm bg-white section-card {extra}" '
            f'id="{key}" aria-labelledby="{key}-title">'
            '<div class="card-body p-4">'
            f'<h2 class="section-title" id="{key}-title">{labels[key]}</h2>'
            f'{content}</div></section>'
        )

    def external(url, label, css=""):
        return f'<a class="{css}" href="{escape(url)}" target="_blank" rel="noopener noreferrer">{label}<span class="external-arrow" aria-hidden="true">↗</span></a>'

    nav_labels = {
        "about": "关于" if zh else "About",
        "experience": "经历" if zh else "Experience",
        "publications": "论文" if zh else "Papers",
        "projects": "项目" if zh else "Projects",
    }
    nav = "".join(
        f'<a class="nav-link" href="#{key}">{nav_labels[key]}</a>'
        for key in ("about", "experience", "publications", "projects")
    )
    interests = "".join(
        f'<div class="research-area"><h3>{text(item["label"])}</h3>'
        f'<p>{text(item["text"])}</p><div class="topic-tags">'
        + "".join(f'<span>{escape(tag)}</span>' for tag in item["tags"])
        + '</div></div>'
        for item in profile["interests"]
    )
    about = section(
        "about",
        f'<p class="intro-text">{text(profile["intro"])}</p>'
        f'<p class="publication-summary">{text(profile["summary"])}</p>'
        f'<div class="research-areas">{interests}</div>',
    )

    def timeline(items):
        return '<ol class="timeline-list">' + "".join(
            '<li class="timeline-item">'
            f'<div class="item-heading"><h4>{text(item["institution"])}</h4>'
            f'<span class="date">{escape(item["date"])}</span></div>'
            f'<p class="item-degree">{text(item["degree"])}</p>'
            f'<p class="item-department">{text(item["department"])}</p></li>'
            for item in items
        ) + '</ol>'

    exp_title = "科研经历" if zh else "Research Experience"
    edu_title = "教育背景" if zh else "Education"
    experience = section(
        "experience",
        '<div class="row experience-columns"><div class="col-lg-6">'
        f'<h3 class="subsection-title">{exp_title}</h3>{timeline(profile["experience"])}'
        '</div><div class="col-lg-6">'
        f'<h3 class="subsection-title">{edu_title}</h3>{timeline(profile["education"])}'
        '</div></div>',
    )

    def authors(value):
        return '; '.join(
            f'<strong>{escape(name.strip())}</strong>'
            if name.strip() in ("Jing Wang", "Wang J") else escape(name.strip())
            for name in value.split(';')
        )

    def paper(item):
        doi = item.get("doi")
        title = external(f'https://doi.org/{doi}', escape(item["title"]), "paper-title-link") if doi else escape(item["title"])
        first = '<span class="first-author">' + ("第一作者" if zh else "First author") + '</span>' if item["first_author"] else ''
        note = f'<p class="paper-note">{text(item["note"])}</p>' if item.get("note") else ''
        link = external(f'https://doi.org/{doi}', "DOI", "paper-resource") if doi else external(
            'https://pubmed.ncbi.nlm.nih.gov/?term=' + quote(item["title"]),
            "PubMed 检索" if zh else "Find on PubMed", "paper-resource",
        )
        return (
            '<article class="paper-item" data-publication>'
            f'<div class="paper-year" aria-label="{item["year"]}">{item["year"]}</div>'
            '<div class="paper-content">'
            f'<h3>{title}</h3><p class="paper-authors">{authors(item["authors"])}</p>'
            f'<p class="paper-journal"><cite>{escape(item["journal"])}</cite>'
            f' · {item["year"]} · {escape(item["citation"])} {first}</p>'
            f'{note}{link}</div></article>'
        )

    selected = sorted([p for p in profile["publications"] if p["first_author"]], key=lambda p: p["year"], reverse=True)
    coauthored = sorted([p for p in profile["publications"] if not p["first_author"]], key=lambda p: p["year"], reverse=True)
    other_label = f'合作作者论文（{len(coauthored)} 篇）' if zh else f'Co-authored publications ({len(coauthored)})'
    pubs = section(
        "publications",
        '<p class="section-description">'
        + ("第一作者论文 · 姓名加粗标示" if zh else "First-author publications · My name is shown in bold")
        + '</p><div class="publication-list">'
        + ''.join(paper(item) for item in selected)
        + '</div><details class="other-publications"><summary>'
        + other_label + '<span class="details-symbol" aria-hidden="true">+</span></summary>'
        + '<div class="publication-list coauthor-list">'
        + ''.join(paper(item) for item in coauthored)
        + '</div></details>',
    )

    projects = section("projects", '<div class="project-list">' + ''.join(
        '<article class="project-item">'
        f'<div class="project-meta"><span class="role-badge {"principal" if i == 0 else ""}">{text(item["role"])}</span>'
        f'<span class="date">{escape(item["date"])}</span></div>'
        f'<h3>{text(item["title"])}</h3>'
        f'<p>{text(item["funder"])}<span class="meta-separator">·</span>{text(item["amount"])}</p></article>'
        for i, item in enumerate(profile["projects"])
    ) + '</div>')

    patents = section("patents", '<ol class="patent-list">' + ''.join(
        f'<li><h3>{text(item["title"])}</h3><p>{text(item["inventors"])}</p>'
        f'<p class="patent-meta"><span>{escape(item["number"])}</span>'
        f'<span class="meta-separator">·</span>{escape(item["date"])}</p></li>'
        for item in profile["patents"]
    ) + '</ol>')

    skills = section("skills", '<dl class="skills-list">' + ''.join(
        f'<div><dt>{text(item["title"])}</dt><dd>{text(item["text"])}</dd></div>'
        for item in profile["skills"]
    ) + '</dl><p class="language-qualification">' + text(profile["language"]) + '</p>')

    awards = section("awards", '<ul class="awards-list">' + ''.join(
        f'<li><span>{text(item["name"])}</span><span class="date">{item["year"]}</span></li>'
        for item in profile["awards"]
    ) + '</ul>')
    contact = section(
        "contact",
        '<p>' + ("欢迎就生物信息学与抗菌材料相关研究、学术合作及教学科研岗位与我联系。" if zh else "For research collaborations in bioinformatics and antimicrobial materials, or teaching and research opportunities, please contact me by email.")
        + f'</p><a class="contact-email" href="mailto:{escape(profile["email"])}">{escape(profile["email"])}</a>',
    )

    menu = '导航菜单' if zh else 'Navigation menu'
    print_label = '打印 / 保存 PDF' if zh else 'Print / Save PDF'
    switch_file = 'en.html' if zh else 'index.html'
    canonical = profile['url'] + ('/' if zh else '/en.html')
    page_title = '王靖 | 生物信息学与抗菌材料' if zh else 'Jing Wang | Bioinformatics & Antimicrobial Materials'
    description = profile['intro'][lang]
    person = {
        '@context': 'https://schema.org', '@type': 'Person',
        'name': 'Jing Wang', 'alternateName': '王靖', 'url': profile['url'],
        'email': 'mailto:' + profile['email'],
        'alumniOf': [ {'@type': 'CollegeOrUniversity', 'name': 'Inner Mongolia University'},
                      {'@type': 'CollegeOrUniversity', 'name': 'Heilongjiang University of Science and Technology'}],
        'knowsAbout': ['Bioinformatics', 'Multi-omics', 'Antimicrobial materials'],
        'sameAs': ['https://github.com/' + profile['github']],
    }
    template = Template((ROOT / 'src/page.html').read_text())
    return template.substitute(
        page_lang='zh-CN' if zh else 'en', page_title=escape(page_title),
        description=escape(description), canonical=escape(canonical),
        structured_data=json.dumps(person, ensure_ascii=False).replace('</', '<\\/'),
        nav_links=nav, name=text(profile['name']), alternate_name=text(profile['alternate_name']),
        field=text(profile['field']), role=text(profile['role']), affiliation=text(profile['affiliation']),
        email=escape(profile['email']), github=escape(profile['github']),
        switch_file=switch_file, switch_label='EN' if zh else '中文',
        switch_lang='en' if zh else 'zh-CN',
        switch_description='Switch to English' if zh else '切换为中文',
        menu=menu, print_label=print_label,
        side_label='个人简介' if zh else 'Profile',
        research_label='研究方向' if zh else 'Research Interests',
        sidebar_interests=''.join(f'<li>{text(i["label"])}</li>' for i in profile['interests']),
        sidebar_contact='邮箱联系' if zh else 'Email',
        content=about + experience + pubs + projects + patents + skills + awards + contact,
        skip='跳至正文' if zh else 'Skip to content',
        back_top='返回顶部' if zh else 'Back to top',
        updated=('更新于 2026 年 10 月' if zh else 'Updated October 2026'),
        year=profile['updated'][:4],
        template_credit='基于' if zh else 'Based on',
    )


def main():
    profile = json.loads((ROOT / 'data/profile.json').read_text())
    for language, filename in [('zh', 'index.html'), ('en', 'en.html')]:
        (ROOT / filename).write_text(render(profile, language))
    base = profile['url']
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n')
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'<url><loc>{base}/{page}</loc><lastmod>{profile["updated"]}</lastmod></url>\n' for page in ['', 'en.html'])
        + '</urlset>\n'
    )
    print('Built index.html and en.html: 11 publications, 3 projects, 2 patents.')


if __name__ == '__main__':
    main()
