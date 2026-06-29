# -*- coding: utf-8 -*-
# PSOLI: translate the 6 remaining pages to Pashto + make language persist across navigation.
# Safe to re-run (skips files already translated).
import io, sys

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, t): io.open(p, "w", encoding="utf-8").write(t)

# ---------- 1) script.js: persist language choice ----------
js = rd("script.js")
if "psoli-lang" not in js:
    js = js.replace("document.body.classList.toggle('lang-ps',ps);",
                    "document.body.classList.toggle('lang-ps',ps);try{localStorage.setItem('psoli-lang',lang);}catch(e){}", 1)
    js = js.replace("psBtn&&psBtn.addEventListener('click',function(){setLang('ps');});",
                    "psBtn&&psBtn.addEventListener('click',function(){setLang('ps');});\ntry{if(localStorage.getItem('psoli-lang')==='ps'){setLang('ps');}}catch(e){}", 1)
    wr("script.js", js); print("script.js: language now persists across pages")
else:
    print("script.js: persistence already present (skip)")

NAV = [("about.html","About Us","زموږ په اړه"),("programs.html","Programs","پروګرامونه"),
       ("events.html","Events","غونډې"),("transparency.html","Transparency","شفافیت"),
       ("contact.html","Contact","اړیکه")]
def menu(active, tag):
    s = '<div class="menu">'
    for h,en,ps in NAV:
        c = ' class="active"' if h==active else ''
        s += ('<a href="%s"%s data-en="%s" data-ps="%s">%s</a>' % (h,c,en,ps,en)) if tag else ('<a href="%s"%s>%s</a>' % (h,c,en))
    return s + '</div>'

OV_O = '  <a href="index.html">Home</a><a href="about.html">About Us</a><a href="programs.html">Programs</a><a href="events.html">Events</a><a href="donate.html">Donate</a><a href="transparency.html">Transparency</a><a href="contact.html">Contact</a>'
OV_N = '  <a href="index.html" data-en="Home" data-ps="کور">Home</a><a href="about.html" data-en="About Us" data-ps="زموږ په اړه">About Us</a><a href="programs.html" data-en="Programs" data-ps="پروګرامونه">Programs</a><a href="events.html" data-en="Events" data-ps="غونډې">Events</a><a href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a><a href="transparency.html" data-en="Transparency" data-ps="شفافیت">Transparency</a><a href="contact.html" data-en="Contact" data-ps="اړیکه">Contact</a>'

FOOT = [
("<p class=\"foot-tag\">Building unity, culture &amp; community. A nonprofit cultural &amp; community society — nonpolitical, nonreligious. Serving Long Island, NY.</p>",
 "<p class=\"foot-tag\" data-en=\"Building unity, culture &amp; community. A nonprofit cultural &amp; community society — nonpolitical, nonreligious. Serving Long Island, NY.\" data-ps=\"د یووالي، کلتور او ټولنې جوړونه. یوه غیرانتفاعي کلتوري او ټولنیزه ټولنه — غیرسیاسي، غیرمذهبي. د لانګ آیلنډ، نیویارک خدمت.\">Building unity, culture &amp; community. A nonprofit cultural &amp; community society — nonpolitical, nonreligious. Serving Long Island, NY.</p>"),
('<div><h4>Explore</h4><a href="about.html">About Us</a><a href="programs.html">Programs</a><a href="events.html">Events</a><a href="transparency.html">Transparency</a></div>',
 '<div><h4 data-en="Explore" data-ps="نور وپلټئ">Explore</h4><a href="about.html" data-en="About Us" data-ps="زموږ په اړه">About Us</a><a href="programs.html" data-en="Programs" data-ps="پروګرامونه">Programs</a><a href="events.html" data-en="Events" data-ps="غونډې">Events</a><a href="transparency.html" data-en="Transparency" data-ps="شفافیت">Transparency</a></div>'),
('<div><h4>Get involved</h4><a href="donate.html">Donate</a><a href="contact.html">Volunteer</a><a href="contact.html">Contact us</a><a href="events.html">Attend an event</a></div>',
 '<div><h4 data-en="Get involved" data-ps="برخه واخلئ">Get involved</h4><a href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a><a href="contact.html" data-en="Volunteer" data-ps="رضاکار">Volunteer</a><a href="contact.html" data-en="Contact us" data-ps="اړیکه ونیسئ">Contact us</a><a href="events.html" data-en="Attend an event" data-ps="غونډه کې ګډون">Attend an event</a></div>'),
('<span><span class="ps">پخیر راغلی</span> · Building unity, culture &amp; community</span>',
 '<span><span class="ps">پخیر راغلی</span> · <span data-en="Building unity, culture &amp; community" data-ps="د یووالي، کلتور او ټولنې جوړونه">Building unity, culture &amp; community</span></span>'),
]
HDR = ('<a class="btn" href="donate.html">Donate</a><button class="burger"',
       '<a class="btn" href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a><button class="burger"')

def eb(en, hint, ps):
    return ('<span class="dash"></span>%s <span class="ps">%s</span>' % (en, hint),
            '<span class="dash"></span><span data-en="%s" data-ps="%s">%s</span> <span class="ps">%s</span>' % (en, ps, en, hint))

def common(active):
    return [(OV_O,OV_N), HDR, (menu(active,False),menu(active,True))] + FOOT

PAGES = {}

PAGES["about.html"] = ("about.html", [
('<h1>About Us</h1><p>A family of Pashtuns who found one another on Long Island — and built a home for our culture and our community here.</p>',
 '<h1 data-en="About Us" data-ps="زموږ په اړه">About Us</h1><p data-en="A family of Pashtuns who found one another on Long Island — and built a home for our culture and our community here." data-ps="د پښتنو یوه کورنۍ چې په لانګ آیلنډ کې یو بل ته راغله — او دلته یې د خپل کلتور او ټولنې لپاره کور جوړ کړ.">A family of Pashtuns who found one another on Long Island — and built a home for our culture and our community here.</p>'),
('<div class="pillar"><b>Our mission</b><span>To preserve Pashtun culture and heritage, and to support the social, educational, and everyday wellbeing of Pashtun families and their neighbors on Long Island.</span></div>',
 '<div class="pillar"><b data-en="Our mission" data-ps="زموږ موخه">Our mission</b><span data-en="To preserve Pashtun culture and heritage, and to support the social, educational, and everyday wellbeing of Pashtun families and their neighbors on Long Island." data-ps="د پښتني کلتور او میراث ساتنه، او په لانګ آیلنډ کې د پښتنو کورنیو او د هغوی د ګاونډیانو د ټولنیز، زده‌کړیز او ورځني هوساینې ملاتړ.">To preserve Pashtun culture and heritage, and to support the social, educational, and everyday wellbeing of Pashtun families and their neighbors on Long Island.</span></div>'),
('<div class="pillar"><b>Our vision</b><span>A united, thriving community where our language and traditions are passed on with pride, and no family stands alone in hard times.</span></div>',
 '<div class="pillar"><b data-en="Our vision" data-ps="زموږ لیدلوری">Our vision</b><span data-en="A united, thriving community where our language and traditions are passed on with pride, and no family stands alone in hard times." data-ps="یوه متحده او پرمختللې ټولنه چې زموږ ژبه او دودونه په ویاړ سره راتلونکي نسل ته لیږدول کیږي، او هیڅ کورنۍ په سختو ورځو کې یوازې نه پاتې کیږي.">A united, thriving community where our language and traditions are passed on with pride, and no family stands alone in hard times.</span></div>'),
('<div class="pillar"><b>Our promise</b><span>Nonpolitical, nonreligious, and open to all — hospitality first, dignity always, and 100% of support going back to the community.</span></div>',
 '<div class="pillar"><b data-en="Our promise" data-ps="زموږ ژمنه">Our promise</b><span data-en="Nonpolitical, nonreligious, and open to all — hospitality first, dignity always, and 100% of support going back to the community." data-ps="غیرسیاسي، غیرمذهبي، او د ټولو لپاره خلاصه — لومړی مېلمه‌پالنه، تل عزت، او سلنه سلنه مرسته بیرته ټولنې ته.">Nonpolitical, nonreligious, and open to all — hospitality first, dignity always, and 100% of support going back to the community.</span></div>'),
eb("Our history","تاریخچه","زموږ تاریخچه"),
('<h3 style="margin-top:8px">How PSOLI began</h3>',
 '<h3 style="margin-top:8px" data-en="How PSOLI began" data-ps="PSOLI څنګه پیل شو">How PSOLI began</h3>'),
('<p>The Pashtuns Society of Long Island began the way most good things do — with a few families who missed home, and decided to build a piece of it here. We come from different cities and valleys, but we share one language, one table, and one idea of what it means to be a good neighbor.</p>',
 '<p data-en="The Pashtuns Society of Long Island began the way most good things do — with a few families who missed home, and decided to build a piece of it here. We come from different cities and valleys, but we share one language, one table, and one idea of what it means to be a good neighbor." data-ps="د لانګ آیلنډ پښتنو ټولنه هم هغسې پیل شوه لکه ډېر ښه کارونه چې پیلیږي — د څو کورنیو له خوا چې د کور ارمان یې درلود او پریکړه یې وکړه چې دلته یې یوه برخه جوړه کړي. موږ له بېلابېلو ښارونو او درو راغلي یو، خو یوه ژبه، یو دسترخوان او د ښه ګاونډي کیدو یو مفهوم سره شریکوو.">The Pashtuns Society of Long Island began the way most good things do — with a few families who missed home, and decided to build a piece of it here. We come from different cities and valleys, but we share one language, one table, and one idea of what it means to be a good neighbor.</p>'),
('<p>What started as backyard picnics and Eid gatherings grew into a registered nonprofit with a cabinet and board of directors, a welcome banner, and a simple goal: bring people together, look after one another, and make sure our children grow up knowing where they come from. Our founding gathering was even covered by <em>Pakistan News</em>.</p>',
 '<p data-en="What started as backyard picnics and Eid gatherings grew into a registered nonprofit with a cabinet and board of directors, a welcome banner, and a simple goal: bring people together, look after one another, and make sure our children grow up knowing where they come from. Our founding gathering was even covered by <em>Pakistan News</em>." data-ps="هغه څه چې د کور شاته تفریحونو او د اختر غونډو په توګه پیل شول، په یوه راجستر شوې غیرانتفاعي اداره بدل شول — له کابینې او بورډ آف ډایرکټرز، د ښه راغلاست بینر، او یوه ساده موخه سره: خلک سره راجمع کول، د یو بل پاملرنه، او دا ډاډ چې زموږ ماشومان په دې پوهیدو سره لوی شي چې له کومه ځایه دي. زموږ د بنسټ غونډه حتی د <em>Pakistan News</em> له خوا هم پوښل شوه.">What started as backyard picnics and Eid gatherings grew into a registered nonprofit with a cabinet and board of directors, a welcome banner, and a simple goal: bring people together, look after one another, and make sure our children grow up knowing where they come from. Our founding gathering was even covered by <em>Pakistan News</em>.</p>'),
eb("Our values &amp; goals","ارزښتونه","زموږ ارزښتونه او موخې"),
('<h2 class="big">What we stand for.</h2>',
 '<h2 class="big" data-en="What we stand for." data-ps="موږ پر څه ولاړ یو.">What we stand for.</h2>'),
('<div class="prog reveal"><h3>Unity</h3><p>One community that shows up for each other — in celebration and in hardship.</p></div>',
 '<div class="prog reveal"><h3 data-en="Unity" data-ps="یووالی">Unity</h3><p data-en="One community that shows up for each other — in celebration and in hardship." data-ps="یوه ټولنه چې د یو بل لپاره حاضریږي — په خوښۍ او په سختۍ کې.">One community that shows up for each other — in celebration and in hardship.</p></div>'),
('<div class="prog reveal"><h3>Culture</h3><p>Keeping Pashto, poetry, music, and hospitality alive for the next generation.</p></div>',
 '<div class="prog reveal"><h3 data-en="Culture" data-ps="کلتور">Culture</h3><p data-en="Keeping Pashto, poetry, music, and hospitality alive for the next generation." data-ps="د راتلونکي نسل لپاره د پښتو، شعر، موسیقۍ او مېلمه‌پالنې ژوندي ساتل.">Keeping Pashto, poetry, music, and hospitality alive for the next generation.</p></div>'),
('<div class="prog reveal"><h3>Service</h3><p>Meals, mentoring, and a helping hand for families and new arrivals who need it.</p></div>',
 '<div class="prog reveal"><h3 data-en="Service" data-ps="خدمت">Service</h3><p data-en="Meals, mentoring, and a helping hand for families and new arrivals who need it." data-ps="د هغو کورنیو او نوي راغلیو لپاره خواړه، لارښوونه او مرستندویه لاس چې اړتیا ورته لري.">Meals, mentoring, and a helping hand for families and new arrivals who need it.</p></div>'),
('<div class="prog reveal"><h3>Dignity</h3><p>Every person is welcomed as an honorable guest — no judgment, no conditions.</p></div>',
 '<div class="prog reveal"><h3 data-en="Dignity" data-ps="عزت">Dignity</h3><p data-en="Every person is welcomed as an honorable guest — no judgment, no conditions." data-ps="هر کس د یوه معزز مېلمه په توګه هرکلی کیږي — نه قضاوت، نه شرطونه.">Every person is welcomed as an honorable guest — no judgment, no conditions.</p></div>'),
eb("Leadership &amp; board","مشران","مشري او بورډ"),
('<h2 class="big">The people behind PSOLI.</h2><p class="lead">Cabinet and Board of Directors, Pashtuns Society of Long Island (Regd).</p>',
 '<h2 class="big" data-en="The people behind PSOLI." data-ps="د PSOLI تر شا خلک.">The people behind PSOLI.</h2><p class="lead" data-en="Cabinet and Board of Directors, Pashtuns Society of Long Island (Regd)." data-ps="کابینه او بورډ آف ډایرکټرز، د لانګ آیلنډ پښتنو ټولنه (راجستر شوې).">Cabinet and Board of Directors, Pashtuns Society of Long Island (Regd).</p>'),
('<div class="role">Senior Vice President</div>',
 '<div class="role" data-en="Senior Vice President" data-ps="لوړپوړی مرستیال">Senior Vice President</div>'),
('<h3>More to come</h3><div class="role">President &amp; cabinet — names &amp; photos to add</div>',
 '<h3 data-en="More to come" data-ps="نور په لاره دي">More to come</h3><div class="role" data-en="President &amp; cabinet — names &amp; photos to add" data-ps="مشر او کابینه — نومونه او عکسونه به ورزیات شي">President &amp; cabinet — names &amp; photos to add</div>'),
('<div class="role">Member, Board of Directors</div>',
 '<div class="role" data-en="Member, Board of Directors" data-ps="غړی، بورډ آف ډایرکټرز">Member, Board of Directors</div>', 'all'),
eb("Service area","سیمه","د خدمت سیمه"),
('<h2 class="big" style="margin:0 auto">Proudly serving Long Island.</h2>',
 '<h2 class="big" style="margin:0 auto" data-en="Proudly serving Long Island." data-ps="په ویاړ سره د لانګ آیلنډ خدمت.">Proudly serving Long Island.</h2>'),
('<p class="lead reveal" style="margin:24px auto 0;text-align:center">Proudly serving Pashtun families and neighbors across Long Island, New York.</p>',
 '<p class="lead reveal" style="margin:24px auto 0;text-align:center" data-en="Proudly serving Pashtun families and neighbors across Long Island, New York." data-ps="په ویاړ سره د نیویارک، لانګ آیلنډ په اوږدو کې د پښتنو کورنیو او ګاونډیانو خدمت.">Proudly serving Pashtun families and neighbors across Long Island, New York.</p>'),
eb("In the press","خبرونه","په رسنیو کې"),
('<h2 class="big" style="margin:0 auto">Our founding made the news.</h2><p class="lead" style="margin:16px auto 0;color:#e9d9b8">Pakistan News covered the launch of the Pashtuns Society of Long Island.</p>',
 '<h2 class="big" style="margin:0 auto" data-en="Our founding made the news." data-ps="زموږ بنسټ خبر جوړ شو.">Our founding made the news.</h2><p class="lead" style="margin:16px auto 0;color:#e9d9b8" data-en="Pakistan News covered the launch of the Pashtuns Society of Long Island." data-ps="Pakistan News د لانګ آیلنډ پښتنو ټولنې د پیل پوښښ وکړ.">Pakistan News covered the launch of the Pashtuns Society of Long Island.</p>'),
('<h2 class="big">Be part of the family.</h2><p>Everyone is welcome. Support our work, or come to our next gathering.</p><div class="hero-cta"><a class="btn" href="donate.html">Donate</a><a class="btn alt" href="contact.html">Contact us</a></div>',
 '<h2 class="big" data-en="Be part of the family." data-ps="د کورنۍ برخه شئ.">Be part of the family.</h2><p data-en="Everyone is welcome. Support our work, or come to our next gathering." data-ps="هرڅوک ته ښه راغلاست. زموږ د کار ملاتړ وکړئ، یا زموږ راتلونکې غونډې ته راشئ.">Everyone is welcome. Support our work, or come to our next gathering.</p><div class="hero-cta"><a class="btn" href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a><a class="btn alt" href="contact.html" data-en="Contact us" data-ps="اړیکه ونیسئ">Contact us</a></div>'),
])

PAGES["programs.html"] = ("programs.html", [
('<h1>Programs &amp; Services</h1><p>Real help for real families — food, mentoring, settling support, and the gatherings that hold us together.</p>',
 '<h1 data-en="Programs &amp; Services" data-ps="پروګرامونه او خدمتونه">Programs &amp; Services</h1><p data-en="Real help for real families — food, mentoring, settling support, and the gatherings that hold us together." data-ps="د ریښتینو کورنیو لپاره ریښتینې مرسته — خواړه، لارښوونه، د مېشت کیدو ملاتړ، او هغه غونډې چې موږ سره یوځای ساتي.">Real help for real families — food, mentoring, settling support, and the gatherings that hold us together.</p>'),
('<b>Who qualifies</b>', '<b data-en="Who qualifies" data-ps="څوک وړ دي">Who qualifies</b>', 'all'),
('<b>How to take part</b>', '<b data-en="How to take part" data-ps="څنګه برخه واخلئ">How to take part</b>', 'all'),
('<b>Hours</b>', '<b data-en="Hours" data-ps="وختونه">Hours</b>', 'all'),
('<b>Location</b>', '<b data-en="Location" data-ps="ځای">Location</b>', 'all'),
('<b>Contact</b>', '<b data-en="Contact" data-ps="اړیکه">Contact</b>', 'all'),
('<span>TBD</span>', '<span data-en="TBD" data-ps="ټاکل کیږي">TBD</span>', 'all'),
('<span>Long Island, NY.</span>', '<span data-en="Long Island, NY." data-ps="لانګ آیلنډ، نیویارک.">Long Island, NY.</span>', 'all'),
('<span class="ptag">Food assistance</span>\n        <h3>Food Pantry</h3>\n        <p>Groceries and warm, home-cooked meals for families going through a hard stretch. We pack boxes, share Eid and Ramadan meals, and run food drives throughout the year — offered with dignity and discretion.</p>',
 '<span class="ptag" data-en="Food assistance" data-ps="خوراکي مرسته">Food assistance</span>\n        <h3 data-en="Food Pantry" data-ps="خوراکي ذخیره">Food Pantry</h3>\n        <p data-en="Groceries and warm, home-cooked meals for families going through a hard stretch. We pack boxes, share Eid and Ramadan meals, and run food drives throughout the year — offered with dignity and discretion." data-ps="د هغو کورنیو لپاره چې سخت وخت تېروي، خوراکي توکي او تود، کوربه‌پاخه خواړه. موږ بکسونه بنډلوو، د اختر او رمضان خواړه وېشو، او په ټول کال کې د خوراک راټولولو کمپاینونه چلوو — په عزت او پټتیا سره وړاندې کیږي.">Groceries and warm, home-cooked meals for families going through a hard stretch. We pack boxes, share Eid and Ramadan meals, and run food drives throughout the year — offered with dignity and discretion.</p>'),
('<span>Any family in need across our service area — no documentation required.</span>',
 '<span data-en="Any family in need across our service area — no documentation required." data-ps="زموږ د خدمت په سیمه کې هره اړمنه کورنۍ — هیڅ سند ته اړتیا نشته.">Any family in need across our service area — no documentation required.</span>'),
('<span>Reach out by email or phone to request a box, or volunteer on a packing day.</span>',
 '<span data-en="Reach out by email or phone to request a box, or volunteer on a packing day." data-ps="د بکس غوښتنې لپاره د بریښنالیک یا تلیفون له لارې اړیکه ونیسئ، یا د بنډلولو په ورځ کې رضاکار شئ.">Reach out by email or phone to request a box, or volunteer on a packing day.</span>'),
('<span class="ptag">Education &amp; youth</span>\n        <h3>Youth Mentoring</h3>\n        <p>Tutoring, guidance, and leadership for the next generation — homework help, college and career advice, and Pashto language and culture circles so our kids grow up grounded and proud.</p>',
 '<span class="ptag" data-en="Education &amp; youth" data-ps="زده‌کړه او ځوانان">Education &amp; youth</span>\n        <h3 data-en="Youth Mentoring" data-ps="د ځوانانو لارښوونه">Youth Mentoring</h3>\n        <p data-en="Tutoring, guidance, and leadership for the next generation — homework help, college and career advice, and Pashto language and culture circles so our kids grow up grounded and proud." data-ps="د راتلونکي نسل لپاره ښوونه، لارښوونه او مشري — د کورنۍ دندې مرسته، د کالج او دندې مشوره، او د پښتو ژبې او کلتور حلقې چې زموږ ماشومان ټینګ او ویاړمن لوی شي.">Tutoring, guidance, and leadership for the next generation — homework help, college and career advice, and Pashto language and culture circles so our kids grow up grounded and proud.</p>'),
('<span>Youth and students from our community families, all ages welcome.</span>',
 '<span data-en="Youth and students from our community families, all ages welcome." data-ps="زموږ د ټولنې له کورنیو ځوانان او زده‌کوونکي، د هرې عمري لپاره ښه راغلاست.">Youth and students from our community families, all ages welcome.</span>'),
('<span>Sign up a student, or volunteer as a tutor or mentor.</span>',
 '<span data-en="Sign up a student, or volunteer as a tutor or mentor." data-ps="یو زده‌کوونکی نوم لیکنه کړئ، یا د ښوونکي یا لارښود په توګه رضاکار شئ.">Sign up a student, or volunteer as a tutor or mentor.</span>'),
('<span class="ptag">Settlement support</span>\n        <h3>Housing &amp; Settling Help</h3>\n        <p>A guiding hand for new arrivals and families in transition — help understanding housing options, paperwork and forms, school enrollment, and connecting to local resources to get settled and steady.</p>',
 '<span class="ptag" data-en="Settlement support" data-ps="د مېشت کیدو ملاتړ">Settlement support</span>\n        <h3 data-en="Housing &amp; Settling Help" data-ps="د استوګنې او مېشت کیدو مرسته">Housing &amp; Settling Help</h3>\n        <p data-en="A guiding hand for new arrivals and families in transition — help understanding housing options, paperwork and forms, school enrollment, and connecting to local resources to get settled and steady." data-ps="د نوي راغلیو او په لیږد کې کورنیو لپاره لارښود لاس — د استوګنې اختیارونو، اسنادو او فورمو په پوهیدو، د ښوونځي نوم لیکنه، او محلي سرچینو سره نښلولو کې مرسته چې مېشت او ثابت شي.">A guiding hand for new arrivals and families in transition — help understanding housing options, paperwork and forms, school enrollment, and connecting to local resources to get settled and steady.</p>'),
('<span>New arrivals and families needing settlement or housing guidance.</span>',
 '<span data-en="New arrivals and families needing settlement or housing guidance." data-ps="نوي راغلي او هغه کورنۍ چې د مېشت کیدو یا استوګنې لارښوونې ته اړتیا لري.">New arrivals and families needing settlement or housing guidance.</span>'),
('<span>Contact us to be matched with a community volunteer who can help.</span>',
 '<span data-en="Contact us to be matched with a community volunteer who can help." data-ps="موږ سره اړیکه ونیسئ ترڅو د ټولنې له یوه رضاکار سره ونښلول شئ چې مرسته وکړي.">Contact us to be matched with a community volunteer who can help.</span>'),
('<span class="ptag">Culture &amp; heritage</span>\n        <h3>Cultural Preservation &amp; Gatherings</h3>\n        <p>Eid celebrations, summer picnics, poetry evenings, and music — the moments that keep our language and traditions alive and give every family a place to belong.</p>',
 '<span class="ptag" data-en="Culture &amp; heritage" data-ps="کلتور او میراث">Culture &amp; heritage</span>\n        <h3 data-en="Cultural Preservation &amp; Gatherings" data-ps="د کلتور ساتنه او غونډې">Cultural Preservation &amp; Gatherings</h3>\n        <p data-en="Eid celebrations, summer picnics, poetry evenings, and music — the moments that keep our language and traditions alive and give every family a place to belong." data-ps="د اختر لمانځنې، د دوبي تفریحونه، د شعر ماښامونه، او موسیقي — هغه شېبې چې زموږ ژبه او دودونه ژوندي ساتي او هرې کورنۍ ته د تړاو ځای ورکوي.">Eid celebrations, summer picnics, poetry evenings, and music — the moments that keep our language and traditions alive and give every family a place to belong.</p>'),
('<span>Open to all — members, families, and guests.</span>',
 '<span data-en="Open to all — members, families, and guests." data-ps="د ټولو لپاره خلاص — غړي، کورنۍ، او مېلمانه.">Open to all — members, families, and guests.</span>'),
('<span>Watch our events page and bring the whole family.</span>',
 '<span data-en="Watch our events page and bring the whole family." data-ps="زموږ د غونډو پاڼه وګورئ او ټوله کورنۍ راولئ.">Watch our events page and bring the whole family.</span>'),
('<span class="ptag">Family support</span>\n        <h3>Family &amp; Emergency Relief</h3>\n        <p>When a family faces a sudden hardship — illness, loss, or crisis — we rally around them with practical and financial support, and with charity drives for relief efforts back home and here.</p>',
 '<span class="ptag" data-en="Family support" data-ps="د کورنۍ ملاتړ">Family support</span>\n        <h3 data-en="Family &amp; Emergency Relief" data-ps="د کورنۍ او بیړنۍ مرسته">Family &amp; Emergency Relief</h3>\n        <p data-en="When a family faces a sudden hardship — illness, loss, or crisis — we rally around them with practical and financial support, and with charity drives for relief efforts back home and here." data-ps="کله چې یوه کورنۍ له ناڅاپي سختۍ سره مخامخ شي — ناروغي، د چا له لاسه ورکول، یا کړکېچ — موږ د عملي او مالي ملاتړ سره ورته ودریږو، او دلته او په وطن کې د مرستو هڅو لپاره د خیریه کمپاینونو سره.">When a family faces a sudden hardship — illness, loss, or crisis — we rally around them with practical and financial support, and with charity drives for relief efforts back home and here.</p>'),
('<span>Community families facing emergencies or hardship.</span>',
 '<span data-en="Community families facing emergencies or hardship." data-ps="د ټولنې هغه کورنۍ چې له بیړنیو حالاتو یا سختۍ سره مخامخ دي.">Community families facing emergencies or hardship.</span>'),
('<span>Request help confidentially, or donate to the relief fund.</span>',
 '<span data-en="Request help confidentially, or donate to the relief fund." data-ps="په محرمانه توګه د مرستې غوښتنه وکړئ، یا د مرستو صندوق ته بسپنه ورکړئ.">Request help confidentially, or donate to the relief fund.</span>'),
('<h2 class="big">Your support makes these real.</h2><p>Every program here runs on volunteers and donations from neighbors like you.</p><div class="hero-cta"><a class="btn" href="donate.html">Donate</a><a class="btn alt" href="contact.html">Volunteer</a></div>',
 '<h2 class="big" data-en="Your support makes these real." data-ps="ستاسو ملاتړ دا کارونه ریښتیني کوي.">Your support makes these real.</h2><p data-en="Every program here runs on volunteers and donations from neighbors like you." data-ps="دلته هر پروګرام ستاسو په څیر ګاونډیانو د رضاکارانو او بسپنو په مرسته چلیږي.">Every program here runs on volunteers and donations from neighbors like you.</p><div class="hero-cta"><a class="btn" href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a><a class="btn alt" href="contact.html" data-en="Volunteer" data-ps="رضاکار">Volunteer</a></div>'),
])

PAGES["donate.html"] = ("donate.html", [
('<h1>Donate</h1><p>Every gift stays in the community — meals on tables, mentors beside our youth, and a hand for families in need.</p>',
 '<h1 data-en="Donate" data-ps="مرسته وکړئ">Donate</h1><p data-en="Every gift stays in the community — meals on tables, mentors beside our youth, and a hand for families in need." data-ps="هره مرسته په ټولنه کې پاتې کیږي — په دسترخوان خواړه، زموږ د ځوانانو تر څنګ لارښود، او د اړمنو کورنیو لپاره لاس.">Every gift stays in the community — meals on tables, mentors beside our youth, and a hand for families in need.</p>'),
('line-height:1.05">Give with Zelle — scan &amp; send</h2>',
 'line-height:1.05" data-en="Give with Zelle — scan &amp; send" data-ps="د زیلي له لارې ورکړئ — سکین او واستوئ">Give with Zelle — scan &amp; send</h2>'),
('>Open Zelle in your bank\'s app, scan the code below, enter any amount, and send. Free, instant, and 100% to PSOLI.</p>',
 ' data-en="Open Zelle in your bank&#39;s app, scan the code below, enter any amount, and send. Free, instant, and 100% to PSOLI." data-ps="په خپل بانک ایپ کې زیلي پرانیزئ، لاندې کوډ سکین کړئ، هره اندازه ولیکئ، او واستوئ. وړیا، سمدستي، او سلنه سلنه PSOLI ته.">Open Zelle in your bank\'s app, scan the code below, enter any amount, and send. Free, instant, and 100% to PSOLI.</p>'),
('<figcaption>Scan inside your bank\'s Zelle</figcaption>',
 '<figcaption data-en="Scan inside your bank&#39;s Zelle" data-ps="د خپل بانک د زیلي دننه یې سکین کړئ">Scan inside your bank\'s Zelle</figcaption>'),
('>or send to our Zelle address</p>',
 ' data-en="or send to our Zelle address" data-ps="یا زموږ د زیلي پتې ته یې واستوئ">or send to our Zelle address</p>'),
('<button type="button" data-copy="pashtunsny25@gmail.com">Copy</button>',
 '<button type="button" data-copy="pashtunsny25@gmail.com" data-en="Copy" data-ps="کاپي">Copy</button>'),
('<span style="font-weight:600;color:#1f4838;display:block;margin-top:10px">Please add your name and "Donation" in the Zelle memo so we can thank you. For monthly giving, set it as a recurring Zelle payment.</span>',
 '<span style="font-weight:600;color:#1f4838;display:block;margin-top:10px" data-en="Please add your name and &quot;Donation&quot; in the Zelle memo so we can thank you. For monthly giving, set it as a recurring Zelle payment." data-ps="مهرباني وکړئ خپل نوم او «بسپنه» د زیلي په یادښت کې ولیکئ ترڅو مننه وکړای شو. د میاشتنۍ ورکړې لپاره، یې د تکراري زیلي تادیې په توګه تنظیم کړئ.">Please add your name and "Donation" in the Zelle memo so we can thank you. For monthly giving, set it as a recurring Zelle payment.</span>'),
eb("Where it goes","چیرته ځي","چیرته لګیږي"),
('<h2 class="big" style="font-size:clamp(1.8rem,4vw,2.6rem)">100% to the community.</h2>',
 '<h2 class="big" style="font-size:clamp(1.8rem,4vw,2.6rem)" data-en="100% to the community." data-ps="سلنه سلنه ټولنې ته.">100% to the community.</h2>'),
('<div><b>Food &amp; meals</b><span>Pantry boxes and warm meals for families facing hard times.</span></div>',
 '<div><b data-en="Food &amp; meals" data-ps="خواړه">Food &amp; meals</b><span data-en="Pantry boxes and warm meals for families facing hard times." data-ps="د سختو ورځو سره مخامخ کورنیو لپاره د خوراک بکسونه او تود خواړه.">Pantry boxes and warm meals for families facing hard times.</span></div>'),
('<div><b>Youth programs</b><span>Tutoring, mentoring, and Pashto &amp; culture for our kids.</span></div>',
 '<div><b data-en="Youth programs" data-ps="د ځوانانو پروګرامونه">Youth programs</b><span data-en="Tutoring, mentoring, and Pashto &amp; culture for our kids." data-ps="زموږ د ماشومانو لپاره ښوونه، لارښوونه، او پښتو او کلتور.">Tutoring, mentoring, and Pashto &amp; culture for our kids.</span></div>'),
('<div><b>Settling &amp; relief</b><span>Help for new arrivals and families hit by emergencies.</span></div>',
 '<div><b data-en="Settling &amp; relief" data-ps="مېشت کیدل او مرسته">Settling &amp; relief</b><span data-en="Help for new arrivals and families hit by emergencies." data-ps="د نوي راغلیو او د بیړنیو حالاتو ښکار شویو کورنیو لپاره مرسته.">Help for new arrivals and families hit by emergencies.</span></div>'),
('<div><b>Gatherings</b><span>Eid events, picnics, and the moments that keep us together.</span></div>',
 '<div><b data-en="Gatherings" data-ps="غونډې">Gatherings</b><span data-en="Eid events, picnics, and the moments that keep us together." data-ps="د اختر مراسم، تفریحونه، او هغه شېبې چې موږ سره یوځای ساتي.">Eid events, picnics, and the moments that keep us together.</span></div>'),
('<h2 class="big">Thank you for standing with us.</h2><p>Big or small, every contribution helps us build a stronger, more caring community on Long Island.</p><div class="hero-cta"><a class="btn alt" href="programs.html">See what you support</a><a class="btn alt" href="contact.html">Questions? Contact us</a></div>',
 '<h2 class="big" data-en="Thank you for standing with us." data-ps="مننه چې زموږ ملګري یاست.">Thank you for standing with us.</h2><p data-en="Big or small, every contribution helps us build a stronger, more caring community on Long Island." data-ps="کوچنۍ وي که لویه، هره مرسته موږ سره مرسته کوي چې په لانګ آیلنډ کې یوه پیاوړې او پاملرنه‌کوونکې ټولنه جوړه کړو.">Big or small, every contribution helps us build a stronger, more caring community on Long Island.</p><div class="hero-cta"><a class="btn alt" href="programs.html" data-en="See what you support" data-ps="وګورئ څه ملاتړ کوئ">See what you support</a><a class="btn alt" href="contact.html" data-en="Questions? Contact us" data-ps="پوښتنې؟ اړیکه ونیسئ">Questions? Contact us</a></div>'),
])

PAGES["events.html"] = ("events.html", [
('<h1>Events</h1><p>Come gather with us — picnics, Eid celebrations, youth nights, and fundraisers. Everyone\'s welcome.</p>',
 '<h1 data-en="Events" data-ps="غونډې">Events</h1><p data-en="Come gather with us — picnics, Eid celebrations, youth nights, and fundraisers. Everyone&#39;s welcome." data-ps="موږ سره راجمع شئ — تفریحونه، د اختر لمانځنې، د ځوانانو شپې، او د مرستو غونډې. هرڅوک ته ښه راغلاست.">Come gather with us — picnics, Eid celebrations, youth nights, and fundraisers. Everyone\'s welcome.</p>'),
eb("Upcoming","راتلونکې","راتلونکې"),
('<h2 class="big">What\'s coming up.</h2><p class="lead">Example layout — send me the real schedule and I\'ll set the dates and details.</p>',
 '<h2 class="big" data-en="What&#39;s coming up." data-ps="څه په لاره دي.">What\'s coming up.</h2><p class="lead" data-en="Example layout — send me the real schedule and I&#39;ll set the dates and details." data-ps="بېلګه‌ییز جوړښت — ریښتینی مهالویش راولېږئ او زه به نېټې او جزئیات تنظیم کړم.">Example layout — send me the real schedule and I\'ll set the dates and details.</p>'),
('<div class="date">— Month</div><h3>Summer family picnic</h3><p>Long Island park · Open to all families</p>',
 '<div class="date" data-en="— Month" data-ps="— میاشت">— Month</div><h3 data-en="Summer family picnic" data-ps="د دوبي کورنۍ تفریح">Summer family picnic</h3><p data-en="Long Island park · Open to all families" data-ps="د لانګ آیلنډ پارک · د ټولو کورنیو لپاره خلاص">Long Island park · Open to all families</p>'),
('<div class="date">— Month</div><h3>Eid gathering</h3><p>Food, music &amp; community</p>',
 '<div class="date" data-en="— Month" data-ps="— میاشت">— Month</div><h3 data-en="Eid gathering" data-ps="د اختر غونډه">Eid gathering</h3><p data-en="Food, music &amp; community" data-ps="خواړه، موسیقي او ټولنه">Food, music &amp; community</p>'),
('<div class="date">— Month</div><h3>Charity fundraiser dinner</h3><p>Supporting our food &amp; relief programs</p>',
 '<div class="date" data-en="— Month" data-ps="— میاشت">— Month</div><h3 data-en="Charity fundraiser dinner" data-ps="د خیریه مرستو ماښامنۍ">Charity fundraiser dinner</h3><p data-en="Supporting our food &amp; relief programs" data-ps="زموږ د خوراک او مرستو پروګرامونو ملاتړ">Supporting our food &amp; relief programs</p>'),
eb("RSVP","حاضري","حاضري"),
('<h2 class="big">Save your family a spot.</h2>',
 '<h2 class="big" data-en="Save your family a spot." data-ps="خپلې کورنۍ ته ځای خوندي کړئ.">Save your family a spot.</h2>'),
('color:#fce9da;margin-top:14px">Let us know you\'re coming so we can plan food and seating. We\'ll send details and reminders.</p>',
 'color:#fce9da;margin-top:14px" data-en="Let us know you&#39;re coming so we can plan food and seating. We&#39;ll send details and reminders." data-ps="موږ ته خبر راکړئ چې راځئ ترڅو د خوراک او کیناستلو پلان جوړ کړو. موږ به جزئیات او یادونې درواستوو.">Let us know you\'re coming so we can plan food and seating. We\'ll send details and reminders.</p>'),
('<label for="n">Name</label><input id="n" type="text" placeholder="Your name">',
 '<label for="n" data-en="Name" data-ps="نوم">Name</label><input id="n" type="text" placeholder="Your name" data-ph-en="Your name" data-ph-ps="ستاسو نوم">'),
('<label for="e">Email</label><input id="e" type="email" placeholder="you@email.com">',
 '<label for="e" data-en="Email" data-ps="بریښنالیک">Email</label><input id="e" type="email" placeholder="you@email.com">'),
('<label for="ev">Which event?</label><input id="ev" type="text" placeholder="e.g. Summer family picnic">',
 '<label for="ev" data-en="Which event?" data-ps="کومه غونډه؟">Which event?</label><input id="ev" type="text" placeholder="e.g. Summer family picnic" data-ph-en="e.g. Summer family picnic" data-ph-ps="لکه د دوبي کورنۍ تفریح">'),
('<label for="g">How many guests?</label><input id="g" type="number" min="1" placeholder="2">',
 '<label for="g" data-en="How many guests?" data-ps="څومره مېلمانه؟">How many guests?</label><input id="g" type="number" min="1" placeholder="2">'),
('<button class="btn" type="submit">Send RSVP</button>',
 '<button class="btn" type="submit" data-en="Send RSVP" data-ps="حاضري واستوئ">Send RSVP</button>'),
eb("Past highlights","تېرې پیښې","تېرې غونډې"),
('<h2 class="big">Look back at our gatherings.</h2><p class="lead">Moments from recent picnics, dinners, and celebrations across the community.</p>',
 '<h2 class="big" data-en="Look back at our gatherings." data-ps="زموږ غونډو ته یوه کتنه.">Look back at our gatherings.</h2><p class="lead" data-en="Moments from recent picnics, dinners, and celebrations across the community." data-ps="د ټولنې په کچه له وروستیو تفریحونو، ماښامنیو، او لمانځنو شېبې.">Moments from recent picnics, dinners, and celebrations across the community.</p>'),
eb("Watch","ویډیو","ویډیو"),
('<h2 class="big">Our community in motion.</h2><p class="lead" style="color:#e9d9b8">Moments from our gatherings, on film.</p>',
 '<h2 class="big" data-en="Our community in motion." data-ps="زموږ ټولنه په حرکت کې.">Our community in motion.</h2><p class="lead" style="color:#e9d9b8" data-en="Moments from our gatherings, on film." data-ps="زموږ د غونډو شېبې، په فلم کې.">Moments from our gatherings, on film.</p>'),
('<h2 class="big">Eat, gather, give back.</h2><p>Our fundraiser dinners and charity drives power the food pantry, youth programs, and relief fund. Join the next one — or support it from home.</p><div class="hero-cta"><a class="btn" href="donate.html">Donate now</a><a class="btn alt" href="contact.html">Host or sponsor</a></div>',
 '<h2 class="big" data-en="Eat, gather, give back." data-ps="وخورئ، راجمع شئ، بیرته ورکړئ.">Eat, gather, give back.</h2><p data-en="Our fundraiser dinners and charity drives power the food pantry, youth programs, and relief fund. Join the next one — or support it from home." data-ps="زموږ د مرستو ماښامنۍ او خیریه کمپاینونه د خوراکي ذخیرې، د ځوانانو پروګرامونو، او د مرستو صندوق چلوي. په راتلونکي کې برخه واخلئ — یا یې له کوره ملاتړ وکړئ.">Our fundraiser dinners and charity drives power the food pantry, youth programs, and relief fund. Join the next one — or support it from home.</p><div class="hero-cta"><a class="btn" href="donate.html" data-en="Donate now" data-ps="همدا اوس مرسته وکړئ">Donate now</a><a class="btn alt" href="contact.html" data-en="Host or sponsor" data-ps="کوربه یا مرستندوی شئ">Host or sponsor</a></div>'),
])

PAGES["transparency.html"] = ("transparency.html", [
('<h1>Transparency</h1><p>We take care with every dollar entrusted to us. Here\'s how we keep our books — and our promises — open.</p>',
 '<h1 data-en="Transparency" data-ps="شفافیت">Transparency</h1><p data-en="We take care with every dollar entrusted to us. Here&#39;s how we keep our books — and our promises — open." data-ps="موږ د هر هغه ډالر پاملرنه کوو چې موږ ته سپارل شوی وي. دلته ګورئ چې موږ څنګه خپل حسابونه — او خپلې ژمنې — خلاصې ساتو.">We take care with every dollar entrusted to us. Here\'s how we keep our books — and our promises — open.</p>'),
eb("Accountability","حسابدهي","حسابورکونه"),
('<h2 class="big">Open books, by design.</h2><p class="lead">As our nonprofit grows, we\'ll publish our reports and filings here so members and donors can see exactly where support goes.</p>',
 '<h2 class="big" data-en="Open books, by design." data-ps="خلاص حسابونه، له بنسټه.">Open books, by design.</h2><p class="lead" data-en="As our nonprofit grows, we&#39;ll publish our reports and filings here so members and donors can see exactly where support goes." data-ps="لکه څنګه چې زموږ غیرانتفاعي اداره وده کوي، موږ به خپل راپورونه او اسناد دلته خپاره کړو ترڅو غړي او بسپنه‌ورکوونکي ووینی چې مرسته دقیقاً چیرته ځي.">As our nonprofit grows, we\'ll publish our reports and filings here so members and donors can see exactly where support goes.</p>'),
('<h3>Annual report</h3><p>A yearly summary of what we did, who we helped, and what we raised and spent.</p><span class="doc">Coming soon</span>',
 '<h3 data-en="Annual report" data-ps="کلنی راپور">Annual report</h3><p data-en="A yearly summary of what we did, who we helped, and what we raised and spent." data-ps="د هغه څه کلنۍ لنډیز چې موږ وکړل، چا سره مو مرسته وکړه، او څومره مو راټول او ولګول.">A yearly summary of what we did, who we helped, and what we raised and spent.</p><span class="doc" data-en="Coming soon" data-ps="ډېر ژر">Coming soon</span>'),
('<h3>IRS filings (Form 990)</h3><p>Once filed, our annual Form 990 will be linked here and available on request.</p><span class="doc">Available on request</span>',
 '<h3 data-en="IRS filings (Form 990)" data-ps="د IRS اسناد (فورم 990)">IRS filings (Form 990)</h3><p data-en="Once filed, our annual Form 990 will be linked here and available on request." data-ps="کله چې وسپارل شي، زموږ کلنی فورم 990 به دلته وتړل شي او د غوښتنې پر بنسټ به شتون ولري.">Once filed, our annual Form 990 will be linked here and available on request.</p><span class="doc" data-en="Available on request" data-ps="د غوښتنې پر بنسټ">Available on request</span>'),
('<h3>Impact reports</h3><p>Stories and numbers from our food, youth, and relief programs as they grow.</p><span class="doc">Coming soon</span>',
 '<h3 data-en="Impact reports" data-ps="د اغیزو راپورونه">Impact reports</h3><p data-en="Stories and numbers from our food, youth, and relief programs as they grow." data-ps="زموږ د خوراک، ځوانانو، او مرستو پروګرامونو کیسې او شمېرې لکه څنګه چې وده کوي.">Stories and numbers from our food, youth, and relief programs as they grow.</p><span class="doc" data-en="Coming soon" data-ps="ډېر ژر">Coming soon</span>'),
('<h3>Where your dollar goes</h3>',
 '<h3 data-en="Where your dollar goes" data-ps="ستاسو ډالر چیرته ځي">Where your dollar goes</h3>'),
('margin:-6px 0 18px">Illustrative allocation — to be replaced with audited figures once our first full year closes.</p>',
 'margin:-6px 0 18px" data-en="Illustrative allocation — to be replaced with audited figures once our first full year closes." data-ps="بېلګه‌ییزه وېش — زموږ د لومړي بشپړ کال له پای ته رسیدو وروسته به د پلټل شویو شمېرو سره بدل شي.">Illustrative allocation — to be replaced with audited figures once our first full year closes.</p>'),
('<span class="nm">Food &amp; meals</span>', '<span class="nm" data-en="Food &amp; meals" data-ps="خواړه">Food &amp; meals</span>'),
('<span class="nm">Youth programs</span>', '<span class="nm" data-en="Youth programs" data-ps="د ځوانانو پروګرامونه">Youth programs</span>'),
('<span class="nm">Family &amp; relief</span>', '<span class="nm" data-en="Family &amp; relief" data-ps="کورنۍ او مرسته">Family &amp; relief</span>'),
('<span class="nm">Events &amp; culture</span>', '<span class="nm" data-en="Events &amp; culture" data-ps="غونډې او کلتور">Events &amp; culture</span>'),
('<span class="nm">Operations</span>', '<span class="nm" data-en="Operations" data-ps="چلونې">Operations</span>'),
('<h2 class="big">Want to see the details?</h2><p>Members and donors can request our records anytime. We\'re glad to share.</p><div class="hero-cta"><a class="btn" href="contact.html">Contact us</a><a class="btn alt" href="donate.html">Donate</a></div>',
 '<h2 class="big" data-en="Want to see the details?" data-ps="جزئیات لیدل غواړئ؟">Want to see the details?</h2><p data-en="Members and donors can request our records anytime. We&#39;re glad to share." data-ps="غړي او بسپنه‌ورکوونکي کولی شي هر وخت زموږ ریکارډونه وغواړي. موږ یې په خوښۍ شریکوو.">Members and donors can request our records anytime. We\'re glad to share.</p><div class="hero-cta"><a class="btn" href="contact.html" data-en="Contact us" data-ps="اړیکه ونیسئ">Contact us</a><a class="btn alt" href="donate.html" data-en="Donate" data-ps="مرسته وکړئ">Donate</a></div>'),
])

PAGES["contact.html"] = ("contact.html", [
('<h1>Get in touch</h1><p>Questions, ideas, ready to volunteer, or need help? We\'d love to hear from you.</p>',
 '<h1 data-en="Get in touch" data-ps="اړیکه ونیسئ">Get in touch</h1><p data-en="Questions, ideas, ready to volunteer, or need help? We&#39;d love to hear from you." data-ps="پوښتنې، نظرونه، د رضاکارۍ لپاره چمتو یاست، یا مرستې ته اړتیا لرئ؟ موږ به ستاسو اوریدل خوښ کړو.">Questions, ideas, ready to volunteer, or need help? We\'d love to hear from you.</p>'),
eb("Reach us","رابطه","موږ ته لاسرسی"),
('<h2 class="big">Say hello.</h2>',
 '<h2 class="big" data-en="Say hello." data-ps="سلام ووایئ.">Say hello.</h2>'),
('<div><b>Email</b><span>pashtunsny25@gmail.com</span></div>',
 '<div><b data-en="Email" data-ps="بریښنالیک">Email</b><span>pashtunsny25@gmail.com</span></div>'),
('<div><b>Phone</b><span>To be added</span></div>',
 '<div><b data-en="Phone" data-ps="تلیفون">Phone</b><span data-en="To be added" data-ps="ورزیاتیږي">To be added</span></div>'),
('<div><b>Service area</b><span>Long Island, NY.</span></div>',
 '<div><b data-en="Service area" data-ps="د خدمت سیمه">Service area</b><span data-en="Long Island, NY." data-ps="لانګ آیلنډ، نیویارک.">Long Island, NY.</span></div>'),
('<div><b>Donate via Zelle</b><span>pashtunsny25@gmail.com</span></div>',
 '<div><b data-en="Donate via Zelle" data-ps="د زیلي له لارې مرسته">Donate via Zelle</b><span>pashtunsny25@gmail.com</span></div>'),
('<label for="n">Name</label><input id="n" type="text" placeholder="Your name">',
 '<label for="n" data-en="Name" data-ps="نوم">Name</label><input id="n" type="text" placeholder="Your name" data-ph-en="Your name" data-ph-ps="ستاسو نوم">'),
('<label for="e">Email</label><input id="e" type="email" placeholder="you@email.com">',
 '<label for="e" data-en="Email" data-ps="بریښنالیک">Email</label><input id="e" type="email" placeholder="you@email.com">'),
('<label for="ph">Phone (optional)</label>',
 '<label for="ph" data-en="Phone (optional)" data-ps="تلیفون (اختیاري)">Phone (optional)</label>'),
('<label for="reason">I\'m reaching out to…</label><input id="reason" type="text" placeholder="Volunteer / Donate / Get help / Question">',
 '<label for="reason" data-en="I&#39;m reaching out to…" data-ps="زه اړیکه نیسم د…">I\'m reaching out to…</label><input id="reason" type="text" placeholder="Volunteer / Donate / Get help / Question" data-ph-en="Volunteer / Donate / Get help / Question" data-ph-ps="رضاکار / مرسته / مرسته غوښتل / پوښتنه">'),
('<label for="m">Message</label><textarea id="m" placeholder="How can we help, or how would you like to get involved?"></textarea>',
 '<label for="m" data-en="Message" data-ps="پیغام">Message</label><textarea id="m" placeholder="How can we help, or how would you like to get involved?" data-ph-en="How can we help, or how would you like to get involved?" data-ph-ps="موږ څنګه مرسته کولی شو، یا تاسو څنګه غواړئ برخه واخلئ؟"></textarea>'),
('<button class="btn" type="submit">Send message</button>',
 '<button class="btn" type="submit" data-en="Send message" data-ps="پیغام واستوئ">Send message</button>'),
eb("Newsletter","خبرتیا","خبرتیا"),
('<h2 class="big">Stay in the loop.</h2><p>Get gathering announcements and community news in your inbox.</p><form onsubmit="return false"><input type="email" placeholder="Your email address" aria-label="Email address"><button class="btn dark" type="submit">Subscribe</button></form>',
 '<h2 class="big" data-en="Stay in the loop." data-ps="په خبر اوسئ.">Stay in the loop.</h2><p data-en="Get gathering announcements and community news in your inbox." data-ps="د غونډو خبرتیاوې او د ټولنې خبرونه خپل بکس ته ترلاسه کړئ.">Get gathering announcements and community news in your inbox.</p><form onsubmit="return false"><input type="email" placeholder="Your email address" data-ph-en="Your email address" data-ph-ps="ستاسو بریښنالیک پته" aria-label="Email address"><button class="btn dark" type="submit" data-en="Subscribe" data-ps="ګډون وکړئ">Subscribe</button></form>'),
])

total = 0
for page, (active, body) in PAGES.items():
    html = rd(page)
    if "data-en" in html:
        print("%-18s already translated (skip)" % page); continue
    reps = common(active) + body
    fail = 0; applied = 0
    for r in reps:
        old, new = r[0], r[1]
        allmode = (len(r) == 3 and r[2] == 'all')
        c = html.count(old)
        if allmode:
            if c == 0: print("  !! [%s] not found:" % page, old[:55]); fail += 1
            else: html = html.replace(old, new); applied += c
        else:
            if c != 1: print("  !! [%s] match=%d:" % (page, c), old[:55]); fail += 1
            else: html = html.replace(old, new); applied += 1
    if fail:
        print("%-18s ABORTED (%d mismatches) — not written" % (page, fail))
    else:
        wr(page, html); total += applied
        print("%-18s OK (%d strings)" % (page, applied))

print("\nDONE. total strings applied:", total)
