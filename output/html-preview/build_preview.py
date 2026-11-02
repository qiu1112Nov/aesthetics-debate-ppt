from pathlib import Path
import json,re,hashlib,shutil
P=Path(__file__).resolve().parent
if (P/'review-status.json').exists() and any(x.get('confirmed') for x in json.loads((P/'review-status.json').read_text())):
 raise SystemExit('存在已确认页：禁止批量覆盖。请先读取审核记录并按授权单页修订。')
slides=[]
def image(f,cls='',style='',alt='真实馆藏山水作品'):
 return f'<img class="{cls}" src="assets/{f}" style="{style}" alt="{alt}">'
def svg(body,w=800,h=400,cls=''):
 return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img"><defs><marker id="arrow{len(slides)}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.5" markerHeight="3.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#A05C4A"/></marker></defs>{body}</svg>'
def arrow(path,extra=''):
 return f'<path d="{path}" class="arrow" marker-end="url(#arrow{len(slides)})" {extra}/>'
def person(x,y):
 return f'<g transform="translate({x} {y})" class="person"><circle cy="-31" r="12"/><path d="M0 -14V27M-24 8L0 -9L23 8M0 27L-18 53M0 27L20 53"/></g>'
def mountain(x=0,y=0,scale=1):
 return f'<g transform="translate({x} {y}) scale({scale})"><path class="m-back" d="M10 310L100 120L150 200L240 30L320 165L370 110L485 310Z"/><path class="m-front" d="M0 320L90 235L145 268L210 150L285 270L350 223L500 320Z"/><path class="contour" d="M240 30L221 130L255 177M210 150L196 237M100 120L132 231"/></g>'
def add(n,title,chapter,speaker,body,take,cls='',source='',basis=''):
 footer=f'<footer><span>{speaker} · {chapter}</span><span>P{n:02d} / 22</span></footer>'
 if n not in (1,22):
  head=f'<header><p class="eyebrow"><i></i>{chapter} / {speaker}</p><h1>{title}</h1></header>'
  content=f'{head}<div class="content {cls}">{body}</div><div class="takeaway">{take}</div>{footer}'
 else: content=body+footer
 slides.append(dict(id=f'P{n:02d}',title=title,chapter=chapter,speaker=speaker,html=f'<section class="slide page-{n:02d} {"cover" if n==1 else ""}" id="P{n:02d}" aria-label="P{n:02d} {title}">{content}</section>',source=source,basis=basis,take=take,version='v0.4-draft',status='待审核',confirmed=False))
ends=json.loads((P/'retained-endpages.json').read_text())
slides.append({**ends[0],'version':ends[0].get('version','v0.4-draft')})
mapdata=[]
def prose(*paragraphs):return '<div class="argument-copy">'+''.join('<p>'+t+'</p>' for t in paragraphs)+'</div>'
def detail(n,judgment,reasons,evidence,link,anchors,removed,layout):
 mapdata.append(dict(page=f'P{n:02d}',judgment=judgment,reasons=reasons,evidence=evidence,contribution=link,lecture_paragraphs=anchors,diagram_changes=removed,layout=layout))
def a(n,title,chapter,speaker,body,take,cls,source,anchors,judgment,reasons,evidence,link,removed,layout):
 add(n,title,chapter,speaker,body,take,'deep '+cls,source,anchors);detail(n,judgment,reasons,evidence,link,anchors,removed,layout)
# P02: one mountain, bodily positions, explanatory prose.
m=svg(mountain(30,40,1.08)+person(53,365)+person(280,290)+person(303,90)+arrow('M83 330L280 90')+arrow('M315 260Q360 215 430 205')+arrow('M343 55L590 55'),650,480)
body=f'<div class="position-study">{m}<p>仰望 · 入谷 · 远眺</p></div>'+prose('站在山脚，我们感到山峰高大；进入山谷，感到幽深；登高远眺，又感到天地辽阔。','同一座山带来不同体验，说明空间的审美意义不只由景物的形状和位置决定，也取决于我们如何观看与行动。','身体位置改变了观看方向，也改变了空间的意义。固定视点下的视觉真实，不能穷尽这一感知过程。')
a(2,'同一座山，体验为何随身体位置改变？','问题提出','一辩',body,'空间审美还须解释身体如何参与感知。','position-layout','','一辩06—10、20—23','身体位置与观看方式参与空间意义的形成。',['仰望、入谷、远眺带来高大、幽深与辽阔的不同感受。','空间意义不仅取决于景物的形状和位置。'],'同一山体三种经验的讲稿情境。','引出完整性标准中不可忽略的身体经验。','三幅重复大山体缩为一幅三位置示意，取消重复标签。','图约35%，文字约65%。')
# P03 balanced concepts, compact diagrams, full sentences.
left=svg('<path class="grid" d="M80 10H720V155H80ZM80 10L400 60L720 10M80 155L400 60L720 155"/><circle class="red-dot" cx="400" cy="60" r="9"/>'+person(400,120)+arrow('M400 83V69'),800,180)
right=svg(mountain(250,10,.45)+mountain(500,35,.34)+person(70,95)+person(400,95)+person(700,95)+arrow('M100 120C200 180 290 150 340 80S480 105 550 70S640 108 675 112','stroke-dasharray="16 10"'),800,180)
body='<div class="concept-essay"><h2>透视：固定视点</h2>'+left+prose('<b>观看方式：</b>从确定位置出发，依几何投影建立远近关系。','<b>空间组织：</b>消失点与比例缩减，使画面具有统一的视觉秩序。','<b>观者角色：</b>面对已组织的空间，判断景物的位置与比例。')+'</div><div class="concept-essay"><h2>身即：身体在场</h2>'+right+prose('<b>观看方式：</b>抬头、前行与回望，使不同方向的经验相互联系。','<b>空间组织：</b>把不同位置的观看经验综合于同一山水画面。','<b>观者角色：</b>以观看、行动、记忆和想象，与空间建立联系。')+'</div>'
a(3,'透视与身即：观看、组织与观者角色','概念界定','一辩',body,'比较典型单点线性透视；“身即”为本组分析概念。','concept-essays','','一辩12—15、20—23','两种空间观区别在于如何组织观看与观者经验。',['透视在确定视点下建立视觉秩序。','身即将身体、观看过程及想象纳入空间联系。'],'讲稿对固定视点／几何投影与身体在场／游观的概念界定。','说明我方比较的不是画面技巧优劣，而是空间经验的解释范围。','保留透视与游观对照图，但缩为短图带；删去重复关键词标签，改为三个维度的句子。','文字与图解比较均衡，文字承担主要论证。')
# P04 preserve exact thesis and three claims; make criterion explicit.
claims=['相较于透视，身即更能呈现空间感知的多维性。','相较于透视，身即更能激发观者对空间的主动参与。','相较于透视，身即更能深化人与空间的精神联系。']
body='<p class="deep-thesis">相较于透视，身即更能实现空间审美的完整性。</p>'+prose('视觉再现是否准确，只回答空间“被看见”的一个维度。衡量审美是否完整，还要看它能否调动人的感知、参与和精神体验。')+'<div class="claim-list">'+''.join(f'<p><b>0{i+1}</b><span>{c}</span></p>' for i,c in enumerate(claims))+'</div>'
a(4,'为什么以“空间审美的完整性”为标准？','论证导航','一辩',body,'以人的完整经验衡量空间审美，而非只比较视觉准确。','criterion-essay','','一辩16—19、24、29、36—39','完整性标准涵盖视觉、身体、参与和精神。',['透视的视觉再现成就值得承认，但视觉真实不是空间审美的全部。','人的感知、参与、精神体验都是评价内容。'],'一辩17的标准原句与三个分论点。','明确三个论点为何在同一评判标准下可比较。','删除概念相加／层层汇合的大图；总论点及三个分论点原文完整保留。','文字为主，细线与编号承担导航。')
# P05: both paintings left, interpretation right.
ath=svg(arrow('M18 38L405 245')+arrow('M790 38L405 245')+arrow('M35 601L405 245')+arrow('M775 601L405 245')+'<circle cx="405" cy="245" r="12" class="red-dot"/>',808,627,'art-overlay')
ear=svg(arrow('M200 548C155 481 265 430 220 360S155 245 195 158','stroke-dasharray="18 12"'),431,627,'art-overlay')
gal=f'<div class="paired-art"><figure><div class="registered athens">{image("school-of-athens.jpg")}{ath}</div><figcaption>《雅典学院》<br>拉斐尔 · [图2]</figcaption></figure><figure><div class="registered early">{image("early-spring.jpg")}{ear}</div><figcaption>《早春图》<br>郭熙 · [图1]</figcaption></figure></div>'
body=gal+prose('<b>《雅典学院》：</b>建筑纵深的透视线汇向统一消失点，清晰组织特定视点下的远近关系。','<b>《早春图》：</b>目光从山脚沿溪流入谷，再仰望高峰、转向远山，综合了不同方向的观看经验。','我方据此主张：空间感知不只是一处视点的统一，也包含观看方向的转换。')
a(5,'作品对读：统一视点与多方向经验','空间认知 · 作品对读','二辩',body,'身即更能呈现人在空间中不断变化的感知经验。','work-essay paired-layout','图1、图2','二辩07—12、27—28','两幅作品组织观看经验的方式不同。',['建筑纵深呈现特定视点下的统一秩序。','山脚、溪谷、高峰与远山引导方向转换。'],'雅典学院建筑透视结构、早春图的山脚—溪谷—高峰—远山。','把作品可见细节接到分论点一。','保留必要透视线与一条游观路径，去掉次要箭头；新增完整比较句。','作品约58%，文字约42%；全幅均等比显示。')
# P06 theory with compact but meaningful diagrams.
art=[]
for label,sub,g in [('高远','自山下而仰山巅',mountain(10,12,.9)+person(45,308)+arrow('M80 280L235 50')),('深远','自山前而窥山后',mountain(80,-10,.75)+mountain(5,100,.75)+person(28,320)+arrow('M72 290C130 300 260 245 290 150','stroke-dasharray="15 10"')),('平远','自近山而望远山',mountain(280,125,.4)+mountain(5,130,.65)+person(95,225)+arrow('M130 200L460 145'))]:
 art.append('<figure>'+svg(g,520,380)+f'<figcaption><b>{label}</b>｜{sub}</figcaption></figure>')
body='<div class="compact-distances">'+''.join(art)+'</div>'+prose('郭熙在《林泉高致》中以仰望、探察与远眺解释三远。它们不仅是构图方式，也说明身体位置和观看方向如何参与空间组织。','单点线性透视统一某一位置上的视觉关系；三远则把不同位置的经验综合起来，因此更能解释空间感知的多维性。')
a(6,'三远法：身体位置如何参与空间组织？','空间认知 · 理论阐释','二辩',body,'三远综合不同位置的观看经验，不是三个消失点。','distances-essay','文1','二辩15—20、27—28','三远把身体位置与观看方向纳入空间组织。',['三种“远”对应仰望、探察、远眺。','多位置经验的综合支持多维感知。'],'林泉高致三远原文，展示分别摘取定义短句。','从术语解释推进到我方多维性判断。','三组图保留但高度减半；删除冗长图解免责标签，把理论意义写成正文。','紧凑三图约35%，论述约65%。')
# P07 full image + two crops, grounded sentences.
gal=f'<div class="spring-evidence"><figure class="evidence-full">{image("early-spring.jpg")}</figure><div class="evidence-crops"><figure>{image("early-detail-near.jpg")}<figcaption>松石建立近景</figcaption></figure><figure>{image("early-detail-peak.jpg")}<figcaption>主峰唤起仰望</figcaption></figure></div><p class="gallery-credit">郭熙 · 台北故宫 · [图1]</p></div>'
body=gal+prose('<b>从近景进入：</b>下方松树与巨石建立近景，山势与溪流又引导目光进入幽深山谷。','<b>向高处与远处转换：</b>主峰唤起仰望，远山与云雾延展空间；观看如同一次山水游历。','这些经验综合于同一画面，使观者在想象中不断转换观看方向。')
a(7,'《早春图》：细节怎样引导观看转换？','空间认知 · 局部分析','二辩',body,'从画面细节到观看过程：多维空间经验由此形成。','work-essay spring-evidence-layout','图1','二辩21—28','早春图不同区域共同引导视线移动。',['松石近景与溪谷引导由外入内。','主峰和远山引导仰望与远眺。'],'原作全幅、近景松石与主峰两个真实裁切。','说明同画面的多方向经验如何支持分论点一。','三个大局部减为两个；删除绕行连接线和重复标签，腾出作品分析文字。','作品约57%，文字约43%。')
# P08 genuine full painting + travelers.
gal=f'<div class="fan-evidence"><figure>{image("fan-kuan.jpg")}<figcaption>范宽 · [图3]</figcaption></figure><figure>{image("fan-travelers.jpg")}<figcaption>山脚行旅局部<br>台北故宫藏</figcaption></figure></div>'
body=gal+prose('<b>画面证据：</b>巍峨主峰占据主要空间，山脚行旅者极其微小，形成强烈的尺度对比。','<b>经验如何生成：</b>微小人物使观者想象人在巨大山川中行走的身体经验，而非只辨认山体的比例。','山体的雄伟因此具有身体感知上的分量：空间审美超出视觉高度的再现。')
a(8,'《溪山行旅图》：尺度为何具有身体分量？','空间认知 · 尺度分析','二辩',body,'人物尺度把山川的雄伟，转为可想象的身体经验。','work-essay fan-evidence-layout','图3','二辩29—32','山体与行旅尺度唤起身体在场的想象。',['主峰与微小行旅构成可见尺度对比。','人物使观者想象在巨大山川中行走。'],'溪山行旅图全幅及真实行旅局部。','多维感知还包含身体与自然尺度的关系。','删除“高度→分量”的空泛箭头和比例框；以两段解释连接画面证据与论点。','作品约57%，论证约43%。')
# P09 participation argument, diagram now subordinate.
body=prose('山路、桥梁与小舟之所以重要，不只因为它们是画中景物；它们还可能引导观者想象自己进入画面。','当目光沿路径探索、把自身经验带入山水时，观者就不只是接受既成空间，也参与空间经验的形成。','因此，我方所说的“参与”包含游观与想象，不等同于实际走进画中，也不只是一种逼真的视觉幻觉。')+'<div class="participation-aside"><h2>从接受到参与</h2><div>观看画面</div><span>↓</span><div>沿路径想象进入</div><span>↓</span><div>带入自身经验</div><p>据讲稿的教学归纳</p></div>'
a(9,'观看为何能够转化为主动参与？','空间体验 · 分论点二','二辩',body,'身即更能激发观者对空间的主动参与。','participation-essay','','一辩25—28；二辩33—40、47—49','画面线索使观者把自身经验带入空间。',['山路、桥梁、小舟可引发进入画面的想象。','游观过程使观者参与经验形成。'],'一辩的路径情境，二辩对长卷观看活动的解释。','给“主动参与”一个可解释的机制，而非仅给流程名称。','四步大流程缩为旁侧三步关系，删去重复编号与关键词；解释由完整句承担。','论证约65%，辅助关系约35%。')
# P10 three real continuous views, prose explains time and agency.
gal='<div class="long-roll-windows">'+''.join(f'<figure>{image("qianli-section.jpg",style=f"object-position:{pos}% 50%") }<figcaption>{i+1:02d} / 连续观看</figcaption></figure>' for i,pos in enumerate([100,50,0]))+'</div>'
body=gal+'<div class="roll-arguments">'+prose('画卷逐段展开：前一段离开视野，后一段山水不断出现。空间不是同一瞬间的全景，而与观看的时间过程相连。')+prose('观者依次观看山峦、江河与桥梁，通过自身的观看活动形成经验。这种连续游观，使视觉接受进一步成为主动参与。')+'</div><p class="roll-credit">王希孟 · 北宋 · 北京故宫 · [图4]　同一画段从右向左连续取景</p>'
a(10,'《千里江山图》：展开长卷，也在形成经验','空间体验 · 长卷游观','二辩',body,'空间也在观看过程中逐渐展开。','roll-essay','图4','二辩35—40','长卷把空间、时间和观看活动联系起来。',['前后景段递次出现，使空间随观看展开。','观者的活动参与了空间经验的形成。'],'千里江山图真实连续画段与讲稿的逐段展开描述。','用观看机制证明分论点二。','保留三真实窗口；删去夸大的数字时间轴，把时间性与参与的关系写成两段解释。','图像与论证约各半。')
# P11 real art plus interpretation.
body=f'<figure class="fuchun-evidence">{image("fuchun-scroll.jpg",style="object-position:76% 50%") }<figcaption>黄公望《富春山居图·无用师卷》局部 · 台北故宫 · [图5]</figcaption></figure><div class="roll-arguments">'+prose('山体、坡岸与水面连续变化，形成有节奏的空间。随着画卷展开，观者仿佛沿富春江前行，在观看中经历山水。')+prose('画家长期观察自然，又以笔墨转化个人感受。观者带着自身经验游观，空间便兼具观看过程与个人精神意味。')+'</div>'
a(11,'《富春山居图》：游观如何连接个人经验？','空间体验 · 长卷节奏','二辩',body,'空间由观看节奏与个人经验共同获得审美意义。','fuchun-essay','图5','二辩41—45、48','长卷节奏和个人感受共同构成艺术空间。',['连续山体坡岸水面形成沿江前行的观看经验。','长期自然观察通过笔墨转化为个人精神意味。'],'富春山居图的山体坡岸水面与讲稿描述。','把主动参与接到观者和画家的经验。','删除三组孤立关键词，保留横向局部并增加观看机制和个人经验解释。','图像约50%，文字约50%。')
# P12 retain chapter calmness but explain inference.
body=prose('<b>第三分论点：</b>相较于透视，身即更能深化人与空间的精神联系。','看见通向山林的小径、隐于树木的亭台，观者会想象沿路进入、在亭中感受山风与流水。','这类经验不依赖精确计算景物距离，却包含情感与精神意义。身即把这种精神参与纳入审美，因而不止于视觉真实。')+f'<figure class="spirit-evidence">{image("early-spring.jpg",style="object-position:32% 55%") }<figcaption>《早春图》局部 · [图1]<br>用于呼应山水情境</figcaption></figure>'
a(12,'空间意境：为何不能止于视觉真实？','空间意境 · 分论点三','三辩',body,'身即将情感与精神参与，纳入空间审美的理解。','spirit-essay','图1（情境配图，不指认具体亭台细节）','三辩04—12','空间还具有情感与精神意义。',['路径与亭台情境引发进入画面的想象。','精神参与不等于精确判断几何距离。'],'讲稿三辩关于小径亭台的假想情境，不伪称配图对应实景。','铺垫画论怎样解释精神联系。','缩小装饰性山水局部，增加“想象—情感意义—我方论点”的推理。','文字约60%，真实山水情境图约40%。')
# P13 quote, interpretation and role in argument, four-can now subordinate.
body='<div class="guoxi-essay"><blockquote>“但可行可望不如可居可游之为得。”<cite>郭熙《林泉高致集·山水训》</cite></blockquote>'+prose('这段论述把山水的价值从值得观看，进一步指向进入其中、游历其中的愿望。','当山水成为可想象的游历与栖居世界，观看便连接了人的精神向往。这正支持我方对审美完整性的扩展。')+'</div><div class="guoxi-aside"><div class="small-four-can"><span>可行</span><span>可望</span><b>可游</b><b>可居</b></div><figure>'+image('early-spring.jpg',style='object-position:45% 90%')+'<figcaption>《早春图》局部 · [图1]</figcaption></figure></div>'
a(13,'郭熙：从值得观看，到愿意游居','空间意境 · 画论解释','三辩',body,'可游可居的愿望，使山水成为精神参与的场所。','guoxi-layout','图1；文1','一辩25—28；四辩20—21（依页面规划置于第三部分）','可游可居说明观者希望与山水建立更深联系。',['画论强调的不止是观看价值，还有进入游历的愿望。','想象性游居使山水成为寄托精神的世界。'],'林泉高致可行可望与可居可游的比较原文。','以画论支持精神联系与完整性标准。','四可大模块缩成一条辅助关系，不再冒充四级发展；新增引文到论点的两步解释。','论证约62%，作品与辅助关系约38%。')
# P14 quote and reasoning from memory/imagining; compact scene only.
scene=svg(person(90,140)+'<path class="grid" d="M120 120H460V330H120Z"/>'+mountain(160,160,.55)+arrow('M115 108L260 185'),560,400)
body='<div class="zongbing-copy"><blockquote>“圣人含道映物，贤者澄怀味象。”<cite>宗炳《画山水序》</cite></blockquote>'+prose('“澄怀味象”强调以心灵、感受与想象体会山水意味，而非眼睛对景物的简单接收。','宗炳晚年难再远游，借山水画延续自然体验。记忆、想象与身体经验，使身体未到之处仍能成为精神游历的空间。')+'</div><aside class="zongbing-aside">'+scene+'<h2>卧游的关键</h2><p>图像连接记忆与想象，<br>延续人与山川的体验。</p><p class="diagram-note">自绘教学示意</p></aside>'
a(14,'宗炳：卧游如何使精神抵达山川？','空间意境 · 澄怀味象','三辩',body,'卧游说明：精神参与也是空间经验的一部分。','zongbing-layout','文2','三辩14—18','卧游使记忆、想象和身体经验延续自然体验。',['澄怀味象不是被动接收，而是心灵体会。','不能远游时，图像仍可延续与山川的联系。'],'画山水序引文及讲稿对宗炳晚年卧游的解释。','说明空间可在精神参与中被体验。','删除三段大流程和重复山体；保留一幅观看图像示意，增加画论释义及论点连接。','文字约65%，辅助图约35%。')
# P15 authentic works + continuity explained, no invented line of influence.
body=f'<div class="woyou-art-pair"><figure>{image("shen-zhou.png",style="object-fit:contain") }<figcaption>明 · 沈周《卧游图册》册页 · [图6]</figcaption></figure><figure>{image("cheng-zhengkui.jpg",style="object-fit:contain") }<figcaption>清 · 程正揆《江山卧游图》 · [图7]</figcaption></figure></div><div class="roll-arguments">'+prose('沈周以不同自然景物供观者翻阅，程正揆也以山水绘画延续精神游历。卧游因此不是停留在宗炳时代的孤立观念。')+prose('从山水图像到记忆与想象，画中空间都可成为精神活动的场所。这条观念线索支持人与空间的持续联系，而非直接师承的证明。')+'</div>'
a(15,'卧游传统：图像何以成为精神活动的场所？','空间意境 · 传统延续','三辩',body,'从观看图像到精神游历，人与山川的联系得以延续。','woyou-tradition-essay','图6（北京故宫）、图7（大都会）','三辩19—23','不同朝代作品延续通过绘画精神游历的传统。',['翻阅自然景物能形成审美体验。','画中空间可容纳记忆、想象和精神活动。'],'沈周卧游图册与程正揆江山卧游图。','用讲稿既有作品支持第三分论点的延续性。','删除孤立宗炳卡片及大箭头，保留两件真实作品并解释延续的内容。','作品约50%—55%，论证约45%—50%。')
# P16 art remains large, quote and two actual inferential paragraphs.
body=f'<figure class="shitao-evidence">{image("shitao-peaks.png",style="object-position:67% 50%") }<figcaption>石涛《搜尽奇峰打草稿图卷》局部 · 北京故宫 · [图8]</figcaption></figure><div class="shitao-reasoning"><blockquote>“山川与予神遇而迹化也。”<cite>《画语录·山川章第八》</cite></blockquote>'+prose('游历、观察与感受，使画家与山川建立精神联系；艺术创作再将这种体验转化为画面形象。','《搜尽奇峰图》将长期自然观察与个人笔墨结合，说明画中山川也承载主体对自然的感知和理解。')+'</div>'
a(16,'石涛：自然经验怎样转化为艺术空间？','空间意境 · 山川神遇','三辩',body,'山川神遇把人与自然的精神联系，转化为画面表达。','shitao-essay','图8；文3','三辩27—33','画中的山川承载主体对自然的感知和理解。',['观察游历与感受建立精神联系。','创作将自然经验转化为个人艺术语言。'],'神遇原句与搜尽奇峰图；不加入尚待核验的题跋论据。','把画论、作品与精神联系连接为推理。','删除三节点箭头，换成引文释义与具体作品的两段说明。','作品与论证各约50%，以实际容纳为准。')
# P17 modern perspective; no fake direct quote or influence.
body=prose('<b>《知觉现象学》的现代视角：</b>身体不只是放在空间里的物体，而是我们感知和理解世界的基本条件。','我们通过位置、方向、行动能力以及与环境的关系认识空间。因此，空间还包含身体能够行动、感知和参与的世界。','这为身即提供解释视角：身体经验与精神参与应纳入审美。但这是一种现代对话，不是对古代山水画的历史影响。')+'<aside class="embodied-aside"><div>身体的位置与行动</div><span>↓</span><div>对环境的感知</div><span>↓</span><div>经验中的空间</div><p>思想转述，非引文</p></aside>'
a(17,'梅洛-庞蒂：身体何以成为空间经验的条件？','空间意境 · 现代对话','三辩',body,'空间也是身体能够行动、感知和参与的世界。','embodied-layout','文4','三辩37—41、46—50','身体知觉为身即提供现代解释视角。',['位置方向与行动能力构成我们认识世界的条件。','空间经验包含身体活动、情绪与记忆。'],'讲稿对知觉现象学的转述，非直接引文。','解释何以将身体与精神参与纳入完整性标准。','删除大三角概念图；改为侧边简链，正文承担哲学观点到我方论点的推理。','文字约67%，辅助关系约33%。')
# P18 folded timeline, explanatory association at each stop.
stages=[('南朝','宗炳','借图像卧游，使记忆与想象延续山川体验。'),('隋（传）','展子虔','《游春图》联系山水与人物游赏活动。'),('北宋','郭熙 / 范宽','三远综合观看方向，行旅尺度唤起身体感受。'),('元','黄公望','连续长卷把观看过程与个人感受相结合。'),('明','沈周','翻阅自然景物的册页，获得审美体验。'),('清','石涛 / 程正揆','神遇与卧游，继续强调人与山川的精神联系。')]
body='<div class="folded-history">'+''.join(f'<div><b>{era}</b><h2>{name}</h2><p>{t}</p></div>' for era,name,t in stages)+'</div>'
a(18,'历史线索：各时期如何连接人与山川？','全场总结 · 历史回望','四辩',body,'这是观念与作品的关联线索，不是单线进步史。','history-essay','','一辩30—35；四辩10—12、20—26','不同阶段共同关注人在观看游历记忆想象中与天地联系。',['各时期各有作品机制与精神议题。','关联线索不等于未经证明的单线进步或直接传承。'],'宗炳、传展子虔、郭熙范宽、黄公望、沈周、石涛程正揆。','回收身即所概括的历史经验及其多样性。','保留时间线但折为两行，每阶段增加完整解释句；不只列人名。','时间线作为组织文字的结构，不再以大留白和标签为主体。')
# P19 recall evidence, not just labels.
rows=[('early-spring.jpg','多维感知','三远法综合仰望、探察与远眺；《溪山行旅图》的微小行旅，又把身体尺度带入山川感知。'),('qianli-section.jpg','主动参与','《千里江山图》与《富春山居图》连续展开，观者随观看过程在想象中游历，参与经验形成。'),('shitao-peaks.png','精神联系','宗炳以卧游连接记忆与想象；石涛以“神遇”解释自然经验如何转成艺术创造。')]
body='<div class="evidence-recap">'+''.join(f'<div><figure>{image(f)}</figure><h2>{h}</h2><p>{t}</p></div>' for f,h,t in rows)+'</div>'
a(19,'三个分论点：分别由什么证据支撑？','全场总结 · 证据回收','四辩',body,'三类证据共同说明：空间审美包含人的完整经验。','recap-essay','图1、图4、图8（均为此前作品局部）','四辩07—24','三个分论点各有具体作品与理论证据。',['多维感知由三远与身体尺度支撑。','参与由长卷展开支撑，精神联系由卧游神遇支撑。'],'三远、溪山行旅、千里江山、富春山居、宗炳卧游、石涛神遇。','回收既有论据，不另增事实。','缩小三大作品卡片为证据缩略图；关键词改为含作品和机制的完整回收句。','论证约70%，真实作品提示约30%。')
# P20 replace sums with criterion and three explanatory rows.
body='<p class="synthesis-premise"><b>判断前提：</b>视觉准确能组织可信空间，但审美完整性还取决于人的感知、参与与精神体验。</p><div class="synthesis-reasons"><div><h2>认知维度</h2><p>多维感知把身体位置与观看方向的变化纳入画面，使空间经验不止于一个固定视点。</p></div><div><h2>体验维度</h2><p>主动参与把观看过程纳入空间形成，观者不只接受画面，也以自身经验游历山水。</p></div><div><h2>意境维度</h2><p>精神联系使空间承载记忆、想象与情感，说明审美意义不能由几何准确单独概括。</p></div></div>'
a(20,'为何三类经验共同支持空间审美的完整性？','全场总结 · 核心论证','四辩',body,'依此完整性标准，身即更能将人的经验纳入空间审美。','synthesis-essay','','四辩05、07—31；三辩46—48','三个分论点共同扩大了对空间审美经验的解释范围。',['认知说明经验如何随位置方向变化。','参与说明经验如何在观看中形成，精神联系说明经验何以具有情感意义。'],'回收前三部分已展示的作品与理论机制，不增加新论据。','在同一完整性标准下共同支撑总论点；不是把三个术语相加当证明。','删除加号、汇合线和大中心框；用判断前提和三段解释阐明共同支持关系。','完整句与论证关系为核心，细线只辅助层级。')
# P21 practical implications grounded in the three questions, no invented examples.
body='<div class="design-implications"><div><b>园林游览</b><p>关注人在路径中怎样前行、仰望与回望；游览体验应从身体行动来理解，而不只从一处静止视点判断。</p></div><div><b>空间设计</b><p>除图纸准确与视觉美观，还要追问人在其中如何感知环境，使人的行动与感受成为设计考量。</p></div><div><b>交互体验</b><p>关注人在数字环境中怎样参与、获得情感与体验，将使用者的活动纳入对空间意义的理解。</p></div></div><p class="implication-note">据讲稿提出的行动、感知、情感三问展开；不指认具体建成案例。</p>'
a(21,'当代启发：从人的行动与感知出发设计空间','全场总结 · 当代延伸','四辩',body,'空间不仅应被准确呈现，也应被充分体验。','implications-essay','','一辩21；四辩32—38','传统空间观启发当代设计关注人的经验。',['园林从移动中的观看理解体验。','公共空间与数字交互应关注行动感知及情感。'],'讲稿园林、公共空间、数字交互环境三个设问。','说明完整性标准对当代理解空间的意义，不增造案例。','删除三幅概念重复示意图，以三类有明确对象的完整设计启发替代。','文字为主，编号／分隔线形成节奏，避免文本框堆叠。')
slides.append({**ends[1],'version':'v0.4-draft'})
# Retained pages get source mapping without introducing extra visible text.
detail(1,'相较于透视，身即更能实现空间审美的完整性。',[], '封面真实早春图局部。','明确题名及我方立场。','一辩03','封面构图与内容不变。','沿用v0.3原版方向。')
detail(22,'透视让空间呈现在眼前，而身即让生命置身于山水之间。',[], '讲稿结辩原句。','简洁结束，不加新论证。','四辩40—43','保留原结辩形式。','沿用v0.3结尾。')
mapdata.sort(key=lambda x:x['page'])
(P/'argument-map.json').write_text(json.dumps(mapdata,ensure_ascii=False,indent=2))
nav='''<nav class="controls" aria-label="演示控制"><button id="prev">← 上一页</button><label>跳转 <input id="jump" type="number" min="1" max="22" value="1" aria-label="跳转页码"></label><span id="counter">01 / 22</span><button id="next">下一页 →</button><button id="overview">总览</button><a id="single" href="pages/P01.html" target="_blank">单页</a><button id="fullscreen">全屏</button><a href="README.md">说明 / 来源</a></nav><dialog id="thumbs"><button id="close-thumbs">关闭总览</button><div class="thumb-grid"></div></dialog>'''
def document(parts,single=False):
 p01_style='<link rel="stylesheet" href="p01-v0.5.css"><link rel="stylesheet" href="p01-v0.6.css">' if any('id="P01"' in part for part in parts) else ''
 return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>从观看山水到栖居山水｜22页待审核初稿</title><link rel="stylesheet" href="styles.css">'+p01_style+'</head><body'+(' data-single="true"' if single else '')+'><main class="viewer"><div class="stage">'+''.join(parts)+'</div></main>'+nav+'<script src="app.js"></script></body></html>'
(P/'index.html').write_text(document([s['html'] for s in slides]))
(P/'pages').mkdir(exist_ok=True)
for s in slides:
 html=document([s['html']],True).replace('href="styles.css"','href="../styles.css"').replace('href="p01-v0.5.css"','href="../p01-v0.5.css"').replace('href="p01-v0.6.css"','href="../p01-v0.6.css"').replace('src="app.js"','src="../app.js"').replace('src="assets/','src="../assets/').replace('href="README.md"','href="../README.md"')
 (P/'pages'/f'{s["id"]}.html').write_text(html)
(P/'review-status.json').write_text(json.dumps([{k:v for k,v in s.items() if k!='html'} for s in slides],ensure_ascii=False,indent=2))
(P/'page-content.json').write_text(json.dumps([{**{k:v for k,v in s.items() if k!='html'},'html_sha256':hashlib.sha256(s['html'].encode()).hexdigest()} for s in slides],ensure_ascii=False,indent=2))
print('Generated',len(slides),'individually authored pages; no page confirmed.')
