# -*- coding: utf-8 -*-
# PSOLI site update: new seal logo, welcome banner, working Pashto toggle (homepage),
# mobile language toggle fix, and mobile 2x2 grid fix. Safe to re-run.
import io, os, sys, subprocess

try:
    from PIL import Image, ImageDraw
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "Pillow"])
    from PIL import Image, ImageDraw

LOGO = "Logo.webp"
if not os.path.exists(LOGO):
    sys.exit("ERROR: put Logo.webp in this folder (the repo root) first, then re-run.")

# ---------- 1) images from Logo.webp ----------
b = Image.open(LOGO).convert("RGBA")
W, H = b.size
sx, sy = W/1568.0, H/784.0
cx, cy, R = 260*sx, 420*sy, 152*((sx+sy)/2)
crop = b.crop((int(cx-R), int(cy-R), int(cx+R), int(cy+R)))
s = crop.size[0]; ss = 4
m = Image.new("L", (s*ss, s*ss), 0); d = ImageDraw.Draw(m)
ins = 3*ss; d.ellipse((ins, ins, s*ss-ins, s*ss-ins), fill=255)
crop.putalpha(m.resize((s, s), Image.LANCZOS))
crop.resize((240, 240), Image.LANCZOS).save("img/seal.png", optimize=True)
Image.open(LOGO).convert("RGB").save("img/welcome-banner.webp", "WEBP", quality=88)
print("images: img/seal.png + img/welcome-banner.webp")

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, t): io.open(p, "w", encoding="utf-8").write(t)

# ---------- 2) script.js: innerHTML swap + lang-ps class + placeholders ----------
js = rd("script.js")
if "lang-ps" not in js:
    old = ('function setLang(lang){var ps=lang===\'ps\';document.documentElement.lang=ps?\'ps\':\'en\';document.documentElement.dir=ps?\'rtl\':\'ltr\';document.body.dir=ps?\'rtl\':\'ltr\';\n'
           '  enBtn&&enBtn.classList.toggle(\'on\',!ps);psBtn&&psBtn.classList.toggle(\'on\',ps);\n'
           '  document.querySelectorAll(\'[data-en]\').forEach(function(el){var t=ps?(el.dataset.ps||el.dataset.en):el.dataset.en;var s=el.querySelector(\'.t\');if(s){s.textContent=t;}else{el.textContent=t;}});}')
    new = ('function setLang(lang){var ps=lang===\'ps\';document.documentElement.lang=ps?\'ps\':\'en\';document.documentElement.dir=ps?\'rtl\':\'ltr\';document.body.dir=ps?\'rtl\':\'ltr\';document.body.classList.toggle(\'lang-ps\',ps);\n'
           '  enBtn&&enBtn.classList.toggle(\'on\',!ps);psBtn&&psBtn.classList.toggle(\'on\',ps);\n'
           '  document.querySelectorAll(\'[data-en]\').forEach(function(el){var t=ps?(el.dataset.ps||el.dataset.en):el.dataset.en;var s=el.querySelector(\'.t\');if(s){s.innerHTML=t;}else{el.innerHTML=t;}});\n'
           '  document.querySelectorAll(\'[data-ph-en]\').forEach(function(el){el.placeholder=ps?(el.dataset.phPs||el.dataset.phEn):el.dataset.phEn;});}')
    assert js.count(old) == 1, "script.js setLang not found as expected"
    wr("script.js", js.replace(old, new)); print("script.js: updated")
else:
    print("script.js: already updated (skip)")

# ---------- 3) styles.css: mobile lang-toggle fix, Pashto block, mobile 2x2 ----------
css = rd("styles.css")
if ".menu,.actions .lang,.actions .btn{display:none}" in css:
    css = css.replace(".menu,.actions .lang,.actions .btn{display:none}", ".menu,.actions .btn{display:none}")
    print("styles.css: mobile language toggle now visible")
if "lang-ps" not in css:
    css += ('\n/* ===== Pashto (پښتو) language mode ===== */\n'
            'body.lang-ps h1,body.lang-ps h2,body.lang-ps h3,body.lang-ps h4,body.lang-ps .big,body.lang-ps .btn,body.lang-ps .menu a,body.lang-ps .overlay a,body.lang-ps p,body.lang-ps .lead,body.lang-ps .tag-row,body.lang-ps .inv a,body.lang-ps .istat .lab,body.lang-ps .cap,body.lang-ps input,body.lang-ps .foot-grid h4,body.lang-ps .foot-grid a,body.lang-ps .foot-tag,body.lang-ps .foot-base{font-family:"Noto Naskh Arabic","Mulish",system-ui,sans-serif!important}\n'
            'body.lang-ps h1,body.lang-ps .big{line-height:1.5}\n'
            'body.lang-ps .tag-row .ps{display:none}\n')
    print("styles.css: Pashto mode styles added")
if "max-width:760px){.inv-grid" not in css:
    css += '@media(max-width:760px){.inv-grid{grid-template-columns:repeat(2,1fr)}.istat-grid{grid-template-columns:repeat(2,1fr)}.fin-cards{grid-template-columns:1fr}}\n'
    print("styles.css: mobile 2x2 grid fix added")
wr("styles.css", css)

# ---------- 4) index.html: welcome banner + Pashto translations ----------
html = rd("index.html")
oldfig = ('    <div class="reveal">\n'
          '      <figure class="framed"><div style="aspect-ratio:4/3;overflow:hidden;border-radius:2px"><img src="img/banner.jpg" alt="PSOLI welcome banner at a community gathering" style="width:100%;height:100%;object-fit:cover"></div><figcaption class="cap">Most welcome to our honorable guests</figcaption></figure>\n'
          '    </div>')
newfig = ('    <div class="reveal">\n'
          '      <figure class="framed"><div style="aspect-ratio:2/1;overflow:hidden;border-radius:2px"><img src="img/welcome-banner.webp" alt="Pashtuns Society of Long Island — most welcome to our honorable guests" style="width:100%;height:100%;object-fit:cover"></div></figure>\n'
          '    </div>')
if "welcome-banner.webp" not in html and oldfig in html:
    html = html.replace(oldfig, newfig); print("index.html: welcome banner placed")

reps = []
def Rp(old, new): reps.append((old, new))

Rp('<div class="menu">\n      <a href="about.html">About Us</a>\n      <a href="programs.html">Programs</a>\n      <a href="events.html">Events</a>\n      <a href="transparency.html">Transparency</a>\n      <a href="contact.html">Contact</a>\n    </div>',
  '<div class="menu">\n      <a href="about.html" data-en="About Us" data-ps="زموږ په اړه">About Us</a>\n      <a href="programs.html" data-en="Programs" data-ps="پروګرامونه">Programs</a>\n      <a href="events.html" data-en="Events" data-ps="غونډې">Events</a>\n      <a href="transparency.html" data-en="Transparency" data-ps="شفافیت">Transparency</a>\n      <a href="contact.html" data-en="Contact" data-ps="اړیکه">Contact</a>\n    </div>')
Rp('<a class="btn" href="donate.html">Donate</a>\n      <button class="burger"',
  '<a class="btn" href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a>\n      <button class="burger"')
Rp('  <a href="index.html">Home</a>\n  <a href="about.html">About Us</a>\n  <a href="programs.html">Programs</a>\n  <a href="events.html">Events</a>\n  <a href="donate.html">Donate</a>\n  <a href="transparency.html">Transparency</a>\n  <a href="contact.html">Contact</a>',
  '  <a href="index.html" data-en="Home" data-ps="کور">Home</a>\n  <a href="about.html" data-en="About Us" data-ps="زموږ په اړه">About Us</a>\n  <a href="programs.html" data-en="Programs" data-ps="پروګرامونه">Programs</a>\n  <a href="events.html" data-en="Events" data-ps="غونډې">Events</a>\n  <a href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a>\n  <a href="transparency.html" data-en="Transparency" data-ps="شفافیت">Transparency</a>\n  <a href="contact.html" data-en="Contact" data-ps="اړیکه">Contact</a>')
Rp('<h1>A home for Pashtun families on <em>Long Island.</em></h1>',
  '<h1 data-en="A home for Pashtun families on <em>Long Island.</em>" data-ps="په <em>لانګ آیلنډ</em> کې د پښتنو کورنیو لپاره یو کور.">A home for Pashtun families on <em>Long Island.</em></h1>')
Rp('<p class="sub">Culture, community, and care — serving Pashtun families and our neighbors across Long Island.</p>',
  '<p class="sub" data-en="Culture, community, and care — serving Pashtun families and our neighbors across Long Island." data-ps="کلتور، ټولنه او پاملرنه — د لانګ آیلنډ په اوږدو کې د پښتنو کورنیو او خپلو ګاونډیانو خدمت.">Culture, community, and care — serving Pashtun families and our neighbors across Long Island.</p>')
Rp('<a class="btn" href="donate.html">Donate</a>\n      <a class="btn alt" href="programs.html">Our programs</a>',
  '<a class="btn" href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a>\n      <a class="btn alt" href="programs.html" data-en="Our programs" data-ps="زموږ پروګرامونه">Our programs</a>')
Rp('  <span>Unity</span><span>Culture</span><span>Community</span><span>Heritage</span><span>Hospitality</span><span>Family</span>\n  <span>Unity</span><span>Culture</span><span>Community</span><span>Heritage</span><span>Hospitality</span><span>Family</span>',
  '  <span data-en="Unity" data-ps="یووالی">Unity</span><span data-en="Culture" data-ps="کلتور">Culture</span><span data-en="Community" data-ps="ټولنه">Community</span><span data-en="Heritage" data-ps="میراث">Heritage</span><span data-en="Hospitality" data-ps="مېلمه‌پالنه">Hospitality</span><span data-en="Family" data-ps="کورنۍ">Family</span>\n  <span data-en="Unity" data-ps="یووالی">Unity</span><span data-en="Culture" data-ps="کلتور">Culture</span><span data-en="Community" data-ps="ټولنه">Community</span><span data-en="Heritage" data-ps="میراث">Heritage</span><span data-en="Hospitality" data-ps="مېلمه‌پالنه">Hospitality</span><span data-en="Family" data-ps="کورنۍ">Family</span>')
def eb(en, hint, ps):
    Rp('<span class="dash"></span>%s <span class="ps">%s</span>' % (en, hint),
      '<span class="dash"></span><span data-en="%s" data-ps="%s">%s</span> <span class="ps">%s</span>' % (en, ps, en, hint))
eb("Who we are","زموږ په اړه","زموږ په اړه")
eb("Our impact","زموږ اغیزه","زموږ اغیزه")
eb("Our programs","زموږ کارونه","زموږ پروګرامونه")
eb("Get involved","برخه واخلئ","برخه واخلئ")
eb("Community","ټولنه","ټولنه")
eb("Newsletter","خبرتیا","خبرتیا")
Rp('<h2 class="big">Preserving heritage. Caring for community.</h2>',
  '<h2 class="big" data-en="Preserving heritage. Caring for community." data-ps="د میراث ساتنه. د ټولنې پاملرنه.">Preserving heritage. Caring for community.</h2>')
Rp('<p>The Pashtuns Society of Long Island is a nonprofit cultural and community organization — <strong>nonpolitical and nonreligious</strong> — built by families who came from different valleys and made a home together here.</p>',
  '<p data-en="The Pashtuns Society of Long Island is a nonprofit cultural and community organization — <strong>nonpolitical and nonreligious</strong> — built by families who came from different valleys and made a home together here." data-ps="د لانګ آیلنډ پښتنو ټولنه یوه غیرانتفاعي کلتوري او ټولنیزه اداره ده — <strong>غیرسیاسي او غیرمذهبي</strong> — چې د بېلابېلو سیمو څخه راغلو کورنیو جوړه کړې او دلته یې یوځای کور جوړ کړی دی.">The Pashtuns Society of Long Island is a nonprofit cultural and community organization — <strong>nonpolitical and nonreligious</strong> — built by families who came from different valleys and made a home together here.</p>')
Rp("<p>We keep our language, hospitality, and traditions alive, and we look after one another: food for families in need, mentoring for our youth, and a helping hand through life's hardest days.</p>",
  '<p data-en="We keep our language, hospitality, and traditions alive, and we look after one another: food for families in need, mentoring for our youth, and a helping hand through life&#39;s hardest days." data-ps="موږ خپله ژبه، مېلمه‌پالنه او دودونه ژوندي ساتو او د یو بل پاملرنه کوو: د اړمنو کورنیو لپاره خواړه، د خپلو ځوانانو لارښوونه، او د ژوند په سختو ورځو کې مرستندویه لاس.">We keep our language, hospitality, and traditions alive, and we look after one another: food for families in need, mentoring for our youth, and a helping hand through life&#39;s hardest days.</p>')
Rp('<a class="btn" href="about.html">Read our story</a>',
  '<a class="btn" href="about.html" data-en="Read our story" data-ps="زموږ کیسه ولولئ">Read our story</a>')
Rp('<h2 class="big">Small society, big heart.</h2>',
  '<h2 class="big" data-en="Small society, big heart." data-ps="وړه ټولنه، لوی زړه.">Small society, big heart.</h2>')
Rp('<div class="lab">Families served</div>', '<div class="lab" data-en="Families served" data-ps="خدمت‌شوې کورنۍ">Families served</div>')
Rp('<div class="lab">Meals shared</div>', '<div class="lab" data-en="Meals shared" data-ps="وېشل‌شوي خواړه">Meals shared</div>')
Rp('<div class="lab">Youth mentored</div>', '<div class="lab" data-en="Youth mentored" data-ps="لارښوونه‌شوي ځوانان">Youth mentored</div>')
Rp('<div class="lab">Events a year</div>', '<div class="lab" data-en="Events a year" data-ps="کلنۍ غونډې">Events a year</div>')
Rp('<h2 class="big">Ways we show up for our community.</h2>',
  '<h2 class="big" data-en="Ways we show up for our community." data-ps="موږ څنګه د خپلې ټولنې ملاتړ کوو.">Ways we show up for our community.</h2>')
Rp('<h3>Food pantry</h3><p>Groceries and warm meals for families facing hard times — no questions, just help.</p>',
  '<h3 data-en="Food pantry" data-ps="خوراکي ذخیره">Food pantry</h3><p data-en="Groceries and warm meals for families facing hard times — no questions, just help." data-ps="د سختو ورځو سره مخامخ کورنیو لپاره خوراکي توکي او تود خواړه — هیڅ پوښتنه نه، یوازې مرسته.">Groceries and warm meals for families facing hard times — no questions, just help.</p>')
Rp('<h3>Youth mentoring</h3><p>Tutoring, guidance, and leadership for the next generation — rooted in Pashto and pride.</p>',
  '<h3 data-en="Youth mentoring" data-ps="د ځوانانو لارښوونه">Youth mentoring</h3><p data-en="Tutoring, guidance, and leadership for the next generation — rooted in Pashto and pride." data-ps="د راتلونکي نسل لپاره ښوونه، لارښوونه او مشري — په پښتو او ویاړ کې ریښه لرونکې.">Tutoring, guidance, and leadership for the next generation — rooted in Pashto and pride.</p>')
Rp('<h3>Housing &amp; settling help</h3><p>Guidance for new arrivals — finding housing, paperwork, and getting on their feet.</p>',
  '<h3 data-en="Housing &amp; settling help" data-ps="د استوګنې او مېشت کیدو مرسته">Housing &amp; settling help</h3><p data-en="Guidance for new arrivals — finding housing, paperwork, and getting on their feet." data-ps="د نوي راغلیو لپاره لارښوونه — د استوګنې موندنه، اداري چارې، او پښو ته ودرېدل.">Guidance for new arrivals — finding housing, paperwork, and getting on their feet.</p>')
Rp('<h3>Culture &amp; gatherings</h3><p>Eid, picnics, poetry and music that keep our heritage alive for every generation.</p>',
  '<h3 data-en="Culture &amp; gatherings" data-ps="کلتور او غونډې">Culture &amp; gatherings</h3><p data-en="Eid, picnics, poetry and music that keep our heritage alive for every generation." data-ps="اختر، تفریحي غونډې، شعر او موسیقي چې زموږ میراث د هر نسل لپاره ژوندی ساتي.">Eid, picnics, poetry and music that keep our heritage alive for every generation.</p>')
Rp('<a class="btn" href="programs.html">See all programs &amp; how to apply</a>',
  '<a class="btn" href="programs.html" data-en="See all programs &amp; how to apply" data-ps="ټول پروګرامونه او د غوښتنلیک طریقه وګورئ">See all programs &amp; how to apply</a>')
Rp('<h2 class="big">There\'s a place for you.</h2>',
  '<h2 class="big" data-en="There&#39;s a place for you." data-ps="ستاسو لپاره ځای شته.">There&#39;s a place for you.</h2>')
Rp('<h3>Donate</h3><p>Your gift funds meals, youth programs, and family support.</p><a href="donate.html">Donate now →</a>',
  '<h3 data-en="Donate" data-ps="مرسته وکړئ">Donate</h3><p data-en="Your gift funds meals, youth programs, and family support." data-ps="ستاسو مرسته خواړه، د ځوانانو پروګرامونه او د کورنیو ملاتړ تمويلوي.">Your gift funds meals, youth programs, and family support.</p><a href="donate.html" data-en="Donate now →" data-ps="همدا اوس مرسته وکړئ →">Donate now →</a>')
Rp('<h3>Volunteer</h3><p>Give your time at a pantry day, picnic, or youth session.</p><a href="contact.html">Join us →</a>',
  '<h3 data-en="Volunteer" data-ps="رضاکار">Volunteer</h3><p data-en="Give your time at a pantry day, picnic, or youth session." data-ps="خپل وخت د خوراک ورځ، تفریح یا د ځوانانو ناسته کې ورکړئ.">Give your time at a pantry day, picnic, or youth session.</p><a href="contact.html" data-en="Join us →" data-ps="موږ سره یوځای شئ →">Join us →</a>')
Rp('<h3>Attend an event</h3><p>Bring your family to our next gathering or fundraiser.</p><a href="events.html">View events →</a>',
  '<h3 data-en="Attend an event" data-ps="غونډه کې ګډون">Attend an event</h3><p data-en="Bring your family to our next gathering or fundraiser." data-ps="خپله کورنۍ زموږ راتلونکې غونډې یا د مرستو غونډې ته راوله.">Bring your family to our next gathering or fundraiser.</p><a href="events.html" data-en="View events →" data-ps="غونډې وګورئ →">View events →</a>')
Rp('<h3>Spread the word</h3><p>Share our mission with friends, family, and neighbors.</p><a href="contact.html">Get in touch →</a>',
  '<h3 data-en="Spread the word" data-ps="خبر خپور کړئ">Spread the word</h3><p data-en="Share our mission with friends, family, and neighbors." data-ps="زموږ موخه له ملګرو، کورنۍ او ګاونډیانو سره شریکه کړئ.">Share our mission with friends, family, and neighbors.</p><a href="contact.html" data-en="Get in touch →" data-ps="اړیکه ونیسئ →">Get in touch →</a>')
Rp('<h2 class="big">Moments from our gatherings.</h2><p class="lead">Real faces, real celebrations — the everyday warmth of our community.</p>',
  '<h2 class="big" data-en="Moments from our gatherings." data-ps="زموږ د غونډو شېبې.">Moments from our gatherings.</h2><p class="lead" data-en="Real faces, real celebrations — the everyday warmth of our community." data-ps="ریښتيني څېرې، ریښتيني لمانځنې — زموږ د ټولنې هره ورځ ګرمي.">Real faces, real celebrations — the everyday warmth of our community.</p>')
Rp('<h2 class="big">Help us keep showing up.</h2>\n    <p>Every gift — one-time or monthly — puts food on a table, a mentor beside a child, and a roof over a new family. 100% goes to the community.</p>',
  '<h2 class="big" data-en="Help us keep showing up." data-ps="زموږ سره مرسته وکړئ چې دا کار روان وساتو.">Help us keep showing up.</h2>\n    <p data-en="Every gift — one-time or monthly — puts food on a table, a mentor beside a child, and a roof over a new family. 100% goes to the community." data-ps="هره مرسته — یووار یا میاشتنۍ — په دسترخوان خواړه، د ماشوم تر څنګ لارښود، او د نوې کورنۍ پر سر چت برابروي. سلنه سلنه ټولنې ته ځي.">Every gift — one-time or monthly — puts food on a table, a mentor beside a child, and a roof over a new family. 100% goes to the community.</p>')
Rp('<div class="hero-cta"><a class="btn" href="donate.html">Donate now</a><a class="btn alt" href="contact.html">Become a volunteer</a></div>',
  '<div class="hero-cta"><a class="btn" href="donate.html" data-en="Donate now" data-ps="همدا اوس مرسته وکړئ">Donate now</a><a class="btn alt" href="contact.html" data-en="Become a volunteer" data-ps="رضاکار شئ">Become a volunteer</a></div>')
Rp('<h2 class="big">Stay in the loop.</h2>\n    <p>Get gathering announcements and community news in your inbox.</p>\n    <form onsubmit="return false"><input type="email" placeholder="Your email address" aria-label="Email address"><button class="btn dark" type="submit">Subscribe</button></form>',
  '<h2 class="big" data-en="Stay in the loop." data-ps="په خبر اوسئ.">Stay in the loop.</h2>\n    <p data-en="Get gathering announcements and community news in your inbox." data-ps="د غونډو خبرتیاوې او د ټولنې خبرونه خپل بکس ته ترلاسه کړئ.">Get gathering announcements and community news in your inbox.</p>\n    <form onsubmit="return false"><input type="email" placeholder="Your email address" data-ph-en="Your email address" data-ph-ps="ستاسو بریښنالیک پته" aria-label="Email address"><button class="btn dark" type="submit" data-en="Subscribe" data-ps="ګډون وکړئ">Subscribe</button></form>')
Rp('<p class="foot-tag">Building unity, culture &amp; community. A nonprofit cultural &amp; community society — nonpolitical, nonreligious. Serving Long Island, NY.</p>',
  '<p class="foot-tag" data-en="Building unity, culture &amp; community. A nonprofit cultural &amp; community society — nonpolitical, nonreligious. Serving Long Island, NY." data-ps="د یووالي، کلتور او ټولنې جوړونه. یوه غیرانتفاعي کلتوري او ټولنیزه ټولنه — غیرسیاسي، غیرمذهبي. د لانګ آیلنډ، نیویارک خدمت.">Building unity, culture &amp; community. A nonprofit cultural &amp; community society — nonpolitical, nonreligious. Serving Long Island, NY.</p>')
Rp('<div><h4>Explore</h4><a href="about.html">About Us</a><a href="programs.html">Programs</a><a href="events.html">Events</a><a href="transparency.html">Transparency</a></div>',
  '<div><h4 data-en="Explore" data-ps="نور وپلټئ">Explore</h4><a href="about.html" data-en="About Us" data-ps="زموږ په اړه">About Us</a><a href="programs.html" data-en="Programs" data-ps="پروګرامونه">Programs</a><a href="events.html" data-en="Events" data-ps="غونډې">Events</a><a href="transparency.html" data-en="Transparency" data-ps="شفافیت">Transparency</a></div>')
Rp('<div><h4>Get involved</h4><a href="donate.html">Donate</a><a href="contact.html">Volunteer</a><a href="contact.html">Contact us</a><a href="events.html">Attend an event</a></div>',
  '<div><h4 data-en="Get involved" data-ps="برخه واخلئ">Get involved</h4><a href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a><a href="contact.html" data-en="Volunteer" data-ps="رضاکار">Volunteer</a><a href="contact.html" data-en="Contact us" data-ps="اړیکه ونیسئ">Contact us</a><a href="events.html" data-en="Attend an event" data-ps="غونډه کې ګډون">Attend an event</a></div>')
Rp('<span><span class="ps">پخیر راغلی</span> · Building unity, culture &amp; community</span>',
  '<span><span class="ps">پخیر راغلی</span> · <span data-en="Building unity, culture &amp; community" data-ps="د یووالي، کلتور او ټولنې جوړونه">Building unity, culture &amp; community</span></span>')

if "data-en" not in html:
    fail = 0
    for old, new in reps:
        if html.count(old) != 1:
            print("!! translation match failed:", old[:60]); fail += 1
        else:
            html = html.replace(old, new)
    if fail: sys.exit("ABORTED: translation strings did not match.")
    print("index.html: %d Pashto translations applied" % len(reps))
else:
    print("index.html: translations already present (skip)")
wr("index.html", html)
print("DONE. Review with the EN/پښتو toggle, then commit & push.")
