#!/usr/bin/env python3
"""Render the bilingual Memphis homepage from profile.json."""
import html
import json
from pathlib import Path
from string import Template
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
HOME = '<span class="folder-icon" aria-hidden="true"><img src="assets/images/home-folder-yellow.svg?v=20261030-memphis" alt="" width="32" height="32"></span>'


def e(value):
    return html.escape(str(value), quote=True)


def render(data, lang):
    style = 'memphis'
    zh = lang == 'zh'
    def t(value):
        return e(value[lang] if isinstance(value, dict) else value)
    def label(chinese, english):
        return chinese if zh else english
    def ext(url, name, css=''):
        return f'<a class="{css}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{name}</a>'
    name = t(data['name'])
    nav = ''.join(f'<a href="#{key}">{label(cn,en)}</a>' for key,cn,en in [
        ('about','概况','About'), ('experience','经历','Experience'),
        ('publications','论文','Papers'), ('projects','项目','Projects'), ('contact','联系','Contact')
    ])
    counterpart = 'en.html' if zh else 'index.html'
    mail = e(data['email'])
    role = t(data['role'])
    # The decorative motif represents two research areas, not quantitative data.
    motif = '''<div class="memphis-art" aria-hidden="true"><span class="art-circle"></span><span class="art-dots"></span><svg class="art-wave" viewBox="0 0 180 34"><path d="M3 18 20 4 37 28 54 4 71 28 88 4 105 28 122 4 139 28 156 4 177 20" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/></svg><span class="art-pill"></span></div>'''
    profile = f'''<aside class="identity-column"><div class="identity">
      <p class="identity-role">{role}</p><h1>{name}</h1><p class="other-name">{t(data['alternate_name'])}</p>
      <div class="identity-rule"></div><p class="identity-field">{t(data['field'])}</p>
      <p class="identity-institution">{t(data['affiliation'])}</p>
      <div class="identity-links"><a href="mailto:{mail}">{mail}</a>{ext('https://github.com/'+data['github'],'GitHub','github-link')}</div>
      <button class="print-button" type="button" data-print>{label('打印 / 保存 PDF','Print / Save PDF')}</button>
      {motif if style=='memphis' else ''}
    </div><div class="side-note"><h2>{label('研究方向','Research interests')}</h2><p>{t(data['interests'][0]['label'])}</p><p>{t(data['interests'][1]['label'])}</p><a href="#contact">{label('学术交流与合作','Research collaborations')}</a></div></aside>'''
    interests = ''.join(f'''<article class="research-area"><h3>{t(item['label'])}</h3><p>{t(item['text'])}</p></article>''' for item in data['interests'])
    about = f'''<section class="block about" id="about" aria-labelledby="about-title"><div class="section-heading"><h2 id="about-title">{label('研究概况','Research profile')}</h2><span class="small-mark" aria-hidden="true"></span></div>
      <p class="intro">{t(data['intro'])}</p><p class="summary">{t(data['summary'])}</p><div class="research-grid">{interests}</div></section>'''
    def career(item, kind):
        return f'''<li class="career-row"><span class="career-date">{e(item['date'])}</span><div class="career-description"><h3>{t(item['institution'])}</h3><p>{t(item['degree'])}</p><p class="secondary">{t(item['department'])}</p></div><span class="career-type">{kind}</span></li>'''
    experience = f'''<section class="block experience" id="experience" aria-labelledby="experience-title"><div class="section-heading"><h2 id="experience-title">{label('科研与教育经历','Experience & education')}</h2></div><ol class="career-list">'''
    experience += ''.join(career(item,label('科研','Research')) for item in data['experience'])
    experience += ''.join(career(item,label('教育','Education')) for item in data['education'])
    experience += '</ol></section>'
    def authors(value):
        return '; '.join(f'<strong>{e(part.strip())}</strong>' if part.strip() in ['Jing Wang','Wang J'] else e(part.strip()) for part in value.split(';'))
    def paper(item):
        doi = item.get('doi')
        title = ext('https://doi.org/'+doi,e(item['title']),'paper-title') if doi else e(item['title'])
        resource = ext('https://doi.org/'+doi,'DOI','resource') if doi else ext('https://pubmed.ncbi.nlm.nih.gov/?term='+quote(item['title']),label('PubMed 检索','Find on PubMed'),'resource')
        badge = f'<span class="first-author">{label("第一作者","First author")}</span>' if item['first_author'] else ''
        return f'''<article class="paper" data-publication><span class="paper-year">{item['year']}</span><div class="paper-body"><h3>{title}</h3><p class="authors">{authors(item['authors'])}</p><p class="venue"><cite>{e(item['journal'])}</cite> · {item['year']} · {e(item['citation'])}</p><div class="paper-links">{badge}{resource}</div></div></article>'''
    first = sorted([item for item in data['publications'] if item['first_author']], key=lambda item:item['year'],reverse=True)
    other = sorted([item for item in data['publications'] if not item['first_author']], key=lambda item:item['year'],reverse=True)
    publications = f'''<section class="block publications" id="publications" aria-labelledby="publications-title"><div class="section-heading"><h2 id="publications-title">{label('学术论文','Publications')}</h2><span class="heading-note">{label('第一作者论文','First-author papers')}</span></div>'''
    publications += ''.join(paper(item) for item in first)
    publications += f'<details class="more-papers"><summary>{label(f"合作作者论文 · {len(other)} 篇",f"Co-authored publications · {len(other)}")}<span aria-hidden="true">+</span></summary>'
    publications += ''.join(paper(item) for item in other)+'</details></section>'
    projects = f'''<section class="block projects" id="projects" aria-labelledby="projects-title"><div class="section-heading"><h2 id="projects-title">{label('科研项目','Research projects')}</h2></div><div class="project-list">'''
    for item in data['projects']:
        projects += f'''<article class="project"><div class="project-top"><span class="project-role">{t(item['role'])}</span><span class="date">{e(item['date'])}</span></div><h3>{t(item['title'])}</h3><p>{t(item['funder'])} · {t(item['amount'])}</p></article>'''
    projects += '</div></section>'
    patents = f'<section class="block patents" id="patents" aria-labelledby="patents-title"><div class="section-heading"><h2 id="patents-title">{label("发明专利","Patents")}</h2></div><ol class="patent-list">'
    for item in data['patents']:
        patents += f'<li><h3>{t(item["title"])}</h3><p>{t(item["inventors"])}</p><p class="secondary">{e(item["number"])} · {e(item["date"])}</p></li>'
    patents += '</ol></section>'
    skills = f'<section class="block skills" id="skills" aria-labelledby="skills-title"><div class="section-heading"><h2 id="skills-title">{label("研究与技术能力","Research skills")}</h2></div><dl>'
    for item in data['skills']:
        skills += f'<div><dt>{t(item["title"])}</dt><dd>{t(item["text"])}</dd></div>'
    skills += f'</dl><p class="secondary">{t(data["language"])}</p></section>'
    awards = f'<section class="block awards" id="awards" aria-labelledby="awards-title"><div class="section-heading"><h2 id="awards-title">{label("荣誉与奖励","Honors & awards")}</h2></div><ul>'
    awards += ''.join(f'<li><span>{t(item["name"])}</span><span class="date">{item["year"]}</span></li>' for item in data['awards'])+'</ul></section>'
    contact = f'''<section class="block contact" id="contact" aria-labelledby="contact-title"><div class="section-heading"><h2 id="contact-title">{label('保持联系','Get in touch')}</h2></div><p>{label('欢迎就生物信息学、抗菌材料相关研究及教学科研岗位与我联系。','For research collaborations in bioinformatics and antimicrobial materials, or teaching and research opportunities, please contact me by email.')}</p><a class="contact-link" href="mailto:{mail}">{mail}</a></section>'''
    content = about + experience + publications + projects + patents + skills + awards + contact
    canonical = data['url'] + ('/' if zh else '/en.html')
    page_title = label('王靖 | 生物信息学与抗菌材料', 'Jing Wang | Bioinformatics & Antimicrobial Materials')
    person = {
        '@context': 'https://schema.org', '@type': 'Person',
        'name': 'Jing Wang', 'alternateName': '王靖', 'url': data['url'],
        'email': 'mailto:' + data['email'],
        'alumniOf': [{'@type': 'CollegeOrUniversity', 'name': 'Inner Mongolia University'},
                     {'@type': 'CollegeOrUniversity', 'name': 'Heilongjiang University of Science and Technology'}],
        'knowsAbout': ['Bioinformatics', 'Multi-omics', 'Antimicrobial materials'],
        'sameAs': ['https://github.com/' + data['github']],
    }
    return Template((ROOT / 'src/page.html').read_text()).substitute(
        page_lang='zh-CN' if zh else 'en', page_title=e(page_title),
        description=t(data['intro']), canonical=e(canonical),
        structured_data=json.dumps(person, ensure_ascii=False).replace('</', '<\\/'),
        skip=label('跳至正文', 'Skip to content'),
        home_label=label('王靖的个人主页', 'Jing Wang personal homepage'),
        home_icon=HOME, name=name, nav_links=nav,
        menu=label('主页导航', 'Main navigation'),
        switch_file=counterpart, switch_lang='en' if zh else 'zh-CN',
        switch_description=label('Switch to English', '切换为中文'),
        switch_label=label('EN', '中文'), identity=profile, content=content,
        year=e(data['updated'][:4]), back_top=label('返回顶部', 'Back to top'),
        template_credit=label('基于', 'Based on'),
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
