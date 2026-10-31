# -*- coding: utf-8 -*-
"""v4 content patch supplement: POEMS_EXTRA
Translate the remaining black-background / white-text (and white-bg black-text)
"story card" screens — sub-chapter opening cards, date cards, Frederica
Bernkastel poems, notebook pages, fragment narration pages, fight flash-cards —
whose English is NOT covered by POEMS in apply_v4.py.

WHAT THESE BLOCKS ARE
---------------------
apply_v4.POEMS covers the 101 quoted `show text "..."` lines (verified: 0
unmatched).  The remaining cards are shown by two other statement forms:

    show text <name>      (87 statements)
    scene text <name>     (25 statements)

where <name> is an `image text <name> = "text/<name>.png"` definition from
script.rpy — the English text is BAKED INTO the card PNG, so it never appears
as a string in the .rpy source.  Each PNG was read and its English transcribed
exactly; the transcription is listed per key in the comment table below.

KEY CONVENTION (mirrors POEMS)
------------------------------
POEMS keys are the exact argument of `show text "..."` (after wrap-tag
stripping).  POEMS_EXTRA keys are the exact argument of `show text <arg>` /
`scene text <arg>` — i.e. the image-text name.  The same consumer code as
apply_poems() works if, for such lines, it looks up POEMS_EXTRA[arg] and
rewrites the statement to  show text "<zh>"  (build the replacement with the
same newq logic: prefix + zh + suffix, escaping backslashes and quotes).
`scene text <name>` lines have no string form; the consumer may turn them into
`show text "<zh>"` right after a `scene black/white`, or redraw the PNG with
the value below.

SPECIAL KEY: the var `tyuui` exists in BOTH projects with DIFFERENT English:
  "tyuui"            -> project   (Q) card:  "This story is a work of fiction."
  "tyuui@project_k"  -> project_k (K) card:  3-line resemblance disclaimer
(the consumer should try "<arg>@<proj>" first, then plain "<arg>").

VALUE FORMAT
------------
One string per card.  Values store the literal two-character sequence
backslash-n (written as \\n in this Python source, exactly like the POEMS
values in apply_v4.py) so the consumer's escaping produces the .rpy escape
inside the string literal and Ren'Py renders a line break; blank lines mirror
the stanza gaps of the original card.  "Frederica Bernkastel" is rendered as
弗雷德里卡·伯恩卡斯特尔; the decorative pseudo-Latin microprint in the lower
right corner of some Bernkastel cards is intentionally omitted.

DELIBERATELY SKIPPED (no dict entry)
------------------------------------
  oni_usoda, usoda     - near-invisible "嘘だっ！" effect graphics (Japanese,
                         no English text; used onik_011 x2 / onik_015, tsum_021)
  oni_ahaha            - red "あはははは…" laughter effect graphic (Japanese;
                         onik_015:935, shown via im.Alpha wrapper)
  maturi_txt8b, maturi_txt9b - pure-black blank cards (mats_022:3351/3354)
  15 image-text defs never displayed at runtime: t_ep1..t_ep12, hima_aka1,
                         hima_aka2, maturi_txt8

KEY -> SOURCE + ENGLISH TABLE
-----------------------------
57a | project_k | meakashi/meak_002.rpy:8 @meak_002 (show text)
     EN: "A.D. 1982"
57b | project_k | meakashi/meak_002.rpy:10 @meak_002 (show text)
     EN: "The fifth year of the series of mysterious deaths in Hinamizawa,
          also known as Oyashiro-sama's curse
          One year prior to Keiichi Maebara's transfer"
58a | project_k | meakashi/meak_015.rpy:8 @meak_015 (show text)
     EN: "A.D. 1983"
58b | project_k | meakashi/meak_015.rpy:10 @meak_015 (show text)
     EN: "The fourth year of the series of mysterious deaths in Hinamizawa,
          also known as Oyashiro-sama's curse
          One year after Satoshi Houjou's disappearance"
kenkei | project | himatsubushi/hima_001.rpy:997 @hima_001 (scene text) [text/kenkei.png]
     EN: "Gogura, XX Prefecture / Prefectural / Public Safety Division"
kouan | project | himatsubushi/hima_001.rpy:724 @hima_001 (scene text) [text/kouan.png]
     EN: "Kasumigaseki, Tokyo / Metropolitan Police Department / Public Safety Division"
okinomiya | project | himatsubushi/hima_001.rpy:1523 @hima_001 ; onikakushi/onik_015_03.rpy:8 @onik_015_03 (scene text)
     EN: "Okinomiya, / XX Prefecture / Okinomiya Police Station"
ma_1 | project_k | matsuribayashi/mats_021.rpy:3430 @mats_021 (show text)
     EN: "I'm Okonogi of the Mountain Dogs !!"
ma_2 | project_k | matsuribayashi/mats_021.rpy:3434 @mats_021 (show text)
     EN: "Good for you."
ma_3 | project_k | matsuribayashi/mats_021.rpy:3439 @mats_021 (show text, white bg)
     EN: "So how much did you get paid, huh ?"
maturi_txt1 | project_k | matsuribayashi/mats_021.rpy:2768 @mats_021
     EN: "...I made it..."
maturi_txt2 | project_k | matsuribayashi/mats_021.rpy:2813 @mats_021
     EN: "Rika-chan"
maturi_txt2b | project_k | matsuribayashi/mats_021.rpy:2816 @mats_021
     EN: "I came"
maturi_txt2c | project_k | matsuribayashi/mats_021.rpy:2820 @mats_021 (with Shake)
     EN: "to help you !"
maturi_txt3 | project_k | matsuribayashi/mats_021.rpy:2969 @mats_021
     EN: "Akasaka goes all out"
maturi_txt3b | project_k | matsuribayashi/mats_021.rpy:2972 @mats_021
     EN: "from the very first shot !"
maturi_txt4 | project_k | matsuribayashi/mats_021.rpy:2976 @mats_021
     EN: "That's why he needs only one shot."
maturi_txt5 | project_k | matsuribayashi/mats_021.rpy:2981 @mats_021 (with Shake)
     EN: "He is unrelenting !!"
maturi_txt6 | project_k | matsuribayashi/mats_021.rpy:3004 @mats_021
     EN: "His power is like"
maturi_txt6b | project_k | matsuribayashi/mats_021.rpy:3009 @mats_021 (white bg)
     EN: "armor / piercing / ammunition."
maturi_txt6c | project_k | matsuribayashi/mats_021.rpy:3010 @mats_021 (white bg)
     EN: "armor / piercing / ammunition."  (same text as 6b, shadow variant)
maturi_txt7 | project_k | matsuribayashi/mats_021.rpy:3224 & 3242 @mats_021
     EN: "...Too light."
maturi_txt9 | project_k | matsuribayashi/mats_022.rpy:3358 @mats_022 (scene text, white bg)
     EN: "in"
maturi_txt10 | project_k | matsuribayashi/mats_022.rpy:3360 @mats_022 (scene text, white bg)
     EN: "heaven"
maturi_txt10b | project_k | matsuribayashi/mats_022.rpy:3361 @mats_022 (scene text, white bg)
     EN: "heaven"  (same text as 10, no-shadow variant)
maturi_txt11 | project_k | matsuribayashi/mats_024.rpy:2580 @mats_024
     EN: "Monster"
maturi_txt13 | project_k | matsuribayashi/mats_011.rpy:846 @mats_011
     EN: "Monster"
meaed1..7 | project_k | meakashi/meakashi_epilogue.rpy:591/597/605/609/619/627/635 (scene text, white bg)
     meaed1 EN: "I wished so many times that everything was a dream.
                 So, I wrote it down, hoping for it to become true."
     meaed2 EN: "Dreams in cartoons are often like this.
                 "There's a huge stack of sweets! I can't possibly eat them"
                 I try to reach for them, but then somebody wakes me up."
     meaed3 EN: "This dream has been a tremendously long one.
                 I must have been sleeping for more than a year."
     meaed4 EN: "Ah, that's right. / I ran away from baseball practice. /
                 I stepped onto the street when the light was red, / and got hit by a motorcycle. /
                 I've been in a coma since then, but I finally woke up."
     meaed5 EN: "When I open my eyes, I see a hospital ceiling. /
                 And Satoshi-kun looks at me from the bedside... /
                 Aha ha ha ha. That's a bit too perfect."
     meaed6 EN: "But it's okay, right? / It's okay for it to end that way, right?"
     meaed7 EN: "I'm sorry... that I was born."  (text at bottom right)
mina_katari1..24 | project_k | minagoroshi/mina_020.rpy:439/441/507/509/511/568/570/573/575/577/
                   640/642/719/721/781/783/785/787/789/791/793/795/797/799 @mina_020 (show text, white bg)
     katari1  EN: "As we ran around frolicking, a lot of people approached Satoko.
                   Some were concerned for her injuries, Some sympathized with how she had been
                   treated so far, and some even insisted she could rely on them if ever in need."
     katari2  EN: "And all of that, must have been disconcertingly fresh, for Satoko, who wasn't
                   used to it. / Satoko said that all the unusual kindness was making her feel
                   uncomfortable instead, but I knew she was just being shy. Right now, this was
                   just what it took for Satoko to truly feel that the village has been reborn."
     katari3  EN: "When Akasaka had arrived, I'd believed what it took to change fate was the
                   power of an influential individual. Or so I thought. / But it turned out that
                   was a misunderstanding."
     katari4  EN: "Individuals don't make miracles. Everyone must come forward to make them
                   happen. That's why when I thought I could defeat fate as long as I had Akasaka
                   by my side-- it was all in my head. / Even if he had been there by my side, we
                   probably wouldn't have been able to do anything and would have only
                   disappointed ourselves."
     katari5  EN: "I'm not saying that Akasaka was at fault-- that's not the point at all. I may
                   have considered him "useless", perhaps. ...even I'm rather astonished at my
                   foul-mouthedness. / Let's forget about such things tonight. It's been a couple
                   of decades--why not celebrate our reunion instead?"
     katari6  EN: "Keiichi got a lot of attention too, wherever he went. / In order to save
                   Satoko, he took the initiative, and hence his leadership abilities were now
                   known throughout the village. Moreover, him persuading the village coucil and
                   Oryou herself were now legendary tales of his heroism."   [sic: coucil]
     katari7  EN: "Everyone had understood just how much Satoko had been ostracized by the whole
                   village. / And they had also understood how unreasonable it was, for it to
                   continue long after the dam war was over. Seeing Keiichi's efforts to break
                   through that taboo so refreshingly, was a glimpse of a new future ahead for
                   the village and his heroic deeds were praised by all, young and old."
     katari8  EN: "With that said, now Keiichi Maebara had become the hot topic amongst the
                   Hinamizawan people. Naturally, everybody wanted a glimpse of this Maebara
                   Keiichi, And hence the bargain auction saw an unprecedent turnout."  [sic]
     katari9  EN: "Even though he started off red-faced, once he got over his shyness, Keiichi
                   showed his true colors. Eliciting rapturous cheers from the crowd with sheer
                   energy and momentum, The Watanagashi of Shouwa 58 of that day became home to
                   a special fervor that was never before seen. / Now Keiichi has the admiration
                   and recognition of the whole village."
     katari10 EN: "Even after this, I'm sure Keiichi will continue to steer the village into new
                   adventures to come. / Having such a young leader appear, has made the village
                   elders rather reassured."
     katari11 EN: "Back in the main tent, having been the last to rush in, were the many
                   influential Sonozakis. / They were all folk we became indebted to yesterday.
                   Except Satoko, everyone bowed their heads. Until just a few days ago, everyone
                   present was someone who could have been bad-mouthing the Houjou family if they
                   had sat down to drink."
     katari12 EN: "But Keiichi had broken through it all. Having reflected upon their thoughtless
                   insensitivities, I doubt any of these people will discriminate against Satoko
                   again. / In fact, they bowed their heads, apologized for their actions, and
                   promised their assistance if anything were to come up jn the future."  [sic: jn]
     katari13 EN: "Keiichi's parents were also at the festival. They were made quite the fuss of
                   for "having such a magnificent son", being the parents of today's big hero. /
                   According to Keiichi, since his parents rarely left the house from being busy,
                   this was a good chance for them interact with the villagers."  [sic]
     katari14 EN: "Keiichi's father had proudly volunteered to make posters for the town council,
                   if the need ever arose. / ...I heard from Keiichi the posters his father makes
                   are so good that people steal them. / I look forward to seeing just what kind
                   of posters they are."
     katari15 EN: "I heard Hanyuu whisper in disbelief that only recently there was a world where
                   Shion tortures Satoko to death. / That horrific world, this happy-ending world,
                   it's all the same Hinamizawa."
     katari16 EN: "I'm sure that the people who only know this world believe unwaveringly that
                   Hinamizawa was destined to have a happy ending. / Only Hanyuu and I know. Only
                   the bystanders know. That here in Hinamizawa, beyond a membrane so thin, that
                   it was even thinner than a goldfish catching-net-- there were worlds which had
                   met tragic ends."
     katari17 EN: "Which is why, I'm certain that we understand better than anybody else just how
                   much of a blessing this world is. / If Keiichi and the others gave in to their
                   temper without fighting side-by-side, this day would have never come."
     katari18 EN: "If Keiichi lost his temper, he would have committed a crime today. The same
                   goes for Shion. She would be a criminal by today. In Rena's case, she would
                   already be three moves ahead and would have finished the burial by now. /
                   ...Only Mion never blew her fuse. I'm not sure whether to call it prudent or
                   cowardly, ...oops, that was uncalled for."
     katari19 EN: "Of course, there was actually a world where I lost it. ...... I ended up
                   getting myself killed. How hopeless. / Anyway, none of those worlds were any
                   good. We weren't able to take back our happy world."
     katari20 EN: "So I'd given up hope. But nobody else had. We all united to bring about the
                   miracle that needed to happen. / A miracle happened, because everyone united."
     katari21 EN: "This might come across as self-aggrandizing ...but I don't think that there
                   would have been a miracle if even just I had given up and denied unity. /
                   During that last call, if I hadn't taken away the phone receiver from Keiichi,
                   I don't think Satoko would have sought our help."
     katari22 EN: "That's it. The miracle that couldn't have happened without everybody coming
                   together. The miracle that wouldn't have been, if even one of us had given up.
                   / It's thanks to Keiichi who taught me how easy it is to break through fate.
                   I, who had given up from the outset."
     katari23 EN: "If everything is fate and there's a meaning to Keiichi's existence, just what
                   is it trying to tell me? / I already knew. The meaning of resisting fate and
                   the means to fight it. / Never again will I give in to fate. Not once more."
     katari24 EN: "The mirror opposite of what Hanyuu told me- not to hold expectations for
                   anything. / Even Hanyuu must be able to cause some sort of miracle if she just
                   believed without giving up. / Or so I tried telling her, but she's stubborn at
                   the oddest times- and evaded me with a simple "au au"."
nort5   | project_k | meakashi/meak_004.rpy:611  @meak_004  (show text)
     EN: "I'm not even allowed to walk freely under the sun. / I met a boy on a sunny day. /
          How come a perverse girl like me... / ...fell in love with his innocence? /
          Notebook Page 5"
nort19  | project_k | meakashi/meak_007.rpy:10   @meak_007  (show text)
     EN: "Some days I see him, some days I don't. / A clear sky gets cloudy. And rain will
          always stop eventually. / I thought his absence was just like that. / But he was
          actually on the verge of a breakdown. / Notebook Page 19"
nort26  | project_k | meakashi/meak_008.rpy:1156 @meak_008  (show text)
     EN: "I'm disgusted by my own childishness. / I just wanted to fill my void. I didn't care
          about him. / Considering that, Satoshi-kun was very generous. / But... I don't know if
          I can forgive Satoko. That's a different story. / Notebook Page 26"
nort27  | project_k | meakashi/meak_011.rpy:872  @meak_011  (show text)
     EN: "I could save Satoshi-kun if I revealed my real identity. / I was aware of the risk. /
          Grandma would certainly capture me if I revealed it. / I didn't think of the
          consequences after that. / Notebook Page 27"
nort43  | project_k | meakashi/meak_014.rpy:686  @meak_014  (show text)
     EN: "Satoshi-kun disappeared. / Not only that, the reason for his disappearance also
          disappeared. / It must've been done by a human being. / I can't accept that he was
          demoned away. / Notebook Page 43"
nort150 | project_k | meakashi/meak_015.rpy:1065 @meak_015  (show text)
     EN: "I haven't opened this notebook in a while. / My feelings have been written down for
          over 150 pages. / This notebook is the key to my heart. / The other me who's been
          sleeping since last year / is slowly waking up... / Notebook Page 150"
nort159 | project_k | meakashi/meak_016.rpy:168  @meak_016  (show text)
     EN: "I never get fed up with life with him. / He's really cute, you know? / We always walk
          together. / But when I stop, he always walks one extra step. / That's so adorable.
          I love it! / Notebook Page 159"
nort165 | project_k | meakashi/meak_017.rpy:113  @meak_017  (show text)
     EN: "My alter ego told me. / That I'm in a demon's stomach. / I wouldn't have woken up if I
          hadn't heard that voice. / I might not have woken up at all. / Notebook Page 165"
nort186 | project_k | meakashi/meak_019.rpy:977  @meak_019  (show text)
     EN: "Nobody can tell us apart. / We're Mion and Shion, perfect twins. / Notebook Page 186"
okaerinasai | project_k | matsuribayashi/mats_024.rpy:2761 @mats_024 (scene text, white bg)
     EN: "Welcome home, mother."
s53 | project | himatsubushi/hima_001.rpy:172 @himatsubushi_prologue (show text)
     EN: "Early Summer, 1978"
s54 | project_k | matsuribayashi/matsuribayashi_kakera_01.rpy:4748 @kakera_13 (show text) [text/54.png]
     EN: "Early summer, 1979 A.D."
s60 | project | himatsubushi/hima_001.rpy:94 @himatsubushi_prologue (scene text) ;
               himatsubushi/hima_004.rpy:8 @hima_004 (show text)
     EN: "Midsummer, 1985"
si_himatsubushi | project | himatsubushi/hima_001.rpy:26 @himatsubushi_prologue (scene text)
     EN: "Who is the criminal, you ask? / Don't we search for them in this story? /
          Who is the criminal, you ask? / Do you even know what the criminal did? /
          Who's the criminal? / Who is the criminal who will kill me now?! / Frederica Bernkastel"
si_maturibayasi_1 | project_k | mats_op.rpy:12 @matsuribayashi_prologue ; mats_025.rpy:780 @higurashi_epilogue (scene text)
     EN: "Everyone is entitled to happiness. / The difficult part is accepting that. /
          Everyone is entitled to happiness. / The difficult part is fulfilling that. /
          I, too, am entitled to happiness. / The difficult part is working out a compromise. /
          Frederica Bernkastel"
si_maturibayasi_2 | project_k | mats_025.rpy:782 @higurashi_epilogue (scene text)
     EN: "Because from now on, / I'm going to live a much much happier life. /
          I'm not going to compromise with just this. / We'll retrieve all the happiness that we
          missed. / 100 years worth for me, / 1000 years worth for you. / Frederica Bernkastel"
si_meakasi | project_k | meakashi/meak_001.rpy:11 @meakashi_prologue (scene text)
     EN: "She dropped her beads in the sand. So the girl cried. / For one hundred years, the girl
          searched the sands. / They might be in the ocean, not the sand. So the girl cried. /
          For one hundred years, the girl searched the ocean. / They might be in the mountains,
          not the ocean. So the girl cried. / How many years will pass before the girl wonders if
          she really dropped them? / Frederica Bernkastel"
si_minagorosi_1 | project_k | minagoroshi/mina_op.rpy:961 @minagoroshi_prologue (show text) [text/si_mina_01.png]
     EN: "I wanted to know what's outside the well. / So I tried to claw my way up from there. /
          I wanted to know what's outside the well. / So I continued to climb even when I fell
          and injured myself. / I finally realize. / The higher I climb, the more pain I feel
          when I fall. / When my curiosity toward the world and my physical pain become equal...
          / I finally understood the meaning of the frog in the well. / Frederica Bernkastel"
si_minagorosi_2 | project_k | minagoroshi/mina_022.rpy:12 @mina_022 (scene text) [text/si_mina_02.png]
     EN: "Please tell me what happened this night. / This is like a box with a cat inside. /
          Please tell me what happened this night. / I don't even know if the cat is alive or
          dead inside the box. / Please tell me what happened this night. / The cat in the box is
          dead. / Frederica Bernkastel"
si_onikakushi | project | onikakushi/onik_op.rpy:12 @onik_op (scene text)
     EN: "Please do not deplore yourself. / Even if the world does not forgive you, I will
          forgive you. / Please do not deplore yourself. / Even if you do not forgive the world,
          I will forgive you. / So please tell me. / What will it take for you, to forgive me? /
          Frederica Bernkastel"
si_tatarigoroshi | project | tatarigoroshi/tata_001.rpy:13 @tatarigoroshi_prologue (show text)
     EN: "The snake in the well was happy. / For it did not care what was outside the well. /
          The snake in the well was happy. / For it had naught to do with what happened outside
          the well. / And you were happy too. / For you did not know what happened outside the
          well. / Frederica Bernkastel"
si_tumihorobosi | project_k | tsumihoroboshi/tsum_op.rpy:16 @tsumihoroboshi_prologue (scene text)
     EN: "The first time, I would try harder to avoid / the inevitable tragedy. / The second
          time, I would be disgusted with / the inevitable tragedy. / The third time, my disgust
          would turn into anguish. / The seventh time, I'd be laughing by then. /
          Frederica Bernkastel"
si_watanagashi | project | watanagashi/wata_001.rpy:13 @wata_001 (show text)
     EN: "I will not quench your thirst. / For you seek the truith and could not accept that.
          [sic: truith] / I will not quench your thirst. / For the truth you desire does not
          exist. / But I still want to quench your thirst. / For I am the one who cast you into
          the desert. / Frederica Bernkastel"
t_ep0 | project | tatarigoroshi/tata_ep02.rpy:8 @tata_ep02 (show text)
     EN: "June xxth, 2003"
takano_1..8 | project_k | minagoroshi/mina_ep.rpy:1117/1182/1215/1235/1343/1615/1628/1635 @mina_ep (show text, white bg)
     takano_1 EN: "Now, my ideals are complete. / This is a literal utopia. / Here, I am a god,
                   and the curse engraved here will be passed on forever."
     takano_2 EN: "A god has reawakened from a long slumber thanks to the dam war, who curses
                   nonbelievers on the sacred night of Watanagashi. / Year after year, that god
                   reawakened. / The mighty Oyashiro-sama awakened. / And so, they regressed to
                   their primitive fear of the curse."
     takano_3 EN: "And nobody doubts the curse of Oyashiro-sama, perfectly revived from within
                   the belly of its corpse. / Now, resurrected into this world. / When you incur
                   Oyashiro-sama's wrath, the cauldron of Hell bursts open, overflowing, and
                   those who flee will breathe their last breath. / With that final judgment, the
                   curse is finally realized!"
     takano_4 EN: "What will be left behind when you die? / The body will rot down to the bone
                   and be crushed into sand. / What more can you leave behind beyond fertilizer
                   for the earth?"
     takano_5 EN: "I will remain. / A name, a great undertaking, a curse left behind. / My
                   presence will be forever deified in this land. / And those who escaped today's
                   curse will be in awe of it. / They'll pass that fear on to others. / The
                   memories of those herds of people, / will sublimate into me, and I will
                   transcend."
     takano_6 EN: "I am Oyashiro-sama. / This is the curse of Oyashiro-sama. / They'll worship,
                   idolize, and fear me. / When I move, they'll beg for no curse, no death. / My
                   work will be historic. / My existence and the history of this curse will be
                   told for ages."
     takano_7 EN: "I've transcended beyond my body of flesh, becoming the curse. / Even if this
                   body decays, / My work will remain in history forever / Now, I've gained
                   immortality."
     takano_8 EN: "Humans, flesh is your curse. / When your body decays, you can't leave anything
                   behind. / Your malice, regrets, fear. / And you'll know my greatness. / I have
                   become Oyashiro-sama. / Now, I've reached the realm of the gods. / Even if my
                   body is destroyed, what I've done here will be passed down forever. / I've
                   achieved eternal life."
tyuui  | project | onikakushi/onik_op.rpy:84 @onik_op ; watanagashi/wata_001.rpy:70 @wata_001 ;
                 tatarigoroshi/tata_001.rpy:71 @tatarigoroshi_prologue ;
                 himatsubushi/hima_001.rpy:505 @himatsubushi_prologue  (show text)
     EN: "This story is a work of fiction."
tyuui@project_k | mats_op.rpy:14 @matsuribayashi_prologue ; tsum_op.rpy:75 @tsumihoroboshi_prologue ;
                 mina_op.rpy:1020 @minagoroshi_prologue ; meak_001.rpy:65 @meakashi_prologue (scene text)
     EN: "This is a work of fiction. / Any resemblance to actual persons or / organizations is
          entirely coincidental."
tyuui2 | project | onikakushi/onik_op.rpy:91 @onik_op ; watanagashi/wata_001.rpy:72 @wata_001 ;
                 tatarigoroshi/tata_001.rpy:73 @tatarigoroshi_prologue  (show text)
     EN: "June XXth, 1983"
title_mea_j | project_k | meakashi/meak_001.rpy:47 @meakashi_prologue (scene chapter meak_1)
     EN: "第五話 目明し編"   (white bg, red text; Japanese chapter number card)
title_mea | project_k | meakashi/meak_001.rpy:49 @meakashi_prologue (scene chapter meak_2)
     EN: "第五話 目明し編"   (white bg, large red text)
title_tsumi_j | project_k | tsumihoroboshi/tsum_op.rpy:54 @tsumihoroboshi_prologue (scene chapter tumi_1)
     EN: "第六話 罪滅し編"
title_tsumi | project_k | tsumihoroboshi/tsum_op.rpy:56 @tsumihoroboshi_prologue (scene chapter tumi_2)
     EN: "第六話 罪滅し編"
title_mina_j | project_k | minagoroshi/mina_op.rpy:1001 @minagoroshi_prologue (scene chapter mina_1)
     EN: "第七話 皆殺し編"
title_mina | project_k | minagoroshi/mina_op.rpy:1003 @minagoroshi_prologue (scene chapter mina_2)
     EN: "第七話 皆殺し編"
"""

POEMS_EXTRA = {
    # ---- date / location / chapter-opening cards ----------------------------
    # 57a: project_k meak_002:8 -- "A.D. 1982"
    "57a": "公元1982年",
    # 57b: project_k meak_002:10 -- fifth year / one year prior to Keiichi's transfer
    "57b": "雏见泽连续离奇死亡事件的第五年，\\n俗称御社神大人的作祟\\n——前原圭一转学而来的一年前",
    # 58a: project_k meak_015:8 -- "A.D. 1983"
    "58a": "公元1983年",
    # 58b: project_k meak_015:10 -- fourth year / one year after Satoshi's disappearance
    "58b": "雏见泽连续离奇死亡事件的第四年，\\n俗称御社神大人的作祟\\n——北条悟史失踪后的一年",
    # kenkei: project hima_001:997 -- Gogura / Prefectural Public Safety Division
    "kenkei": "谷仓，XX县\\n\\n县警察本部\\n公安课",
    # kouan: project hima_001:724 -- Kasumigaseki / Metropolitan Police Dept.
    "kouan": "东京都·霞关\\n\\n警视厅\\n公安部",
    # okinomiya: project hima_001:1523 + onik_015_03:8 -- Okinomiya Police Station
    "okinomiya": "兴宫，\\nXX县\\n\\n兴宫警察署",
    # s53: project hima_001:172 -- "Early Summer, 1978"
    "s53": "1978年 初夏",
    # s54: project_k matsuribayashi_kakera_01:4748 -- "Early summer, 1979 A.D."
    "s54": "公元1979年 初夏",
    # s60: project hima_001:94 + hima_004:8 -- "Midsummer, 1985"
    "s60": "1985年 盛夏",
    # t_ep0: project tata_ep02:8 -- "June xxth, 2003"
    "t_ep0": "2003年6月XX日",
    # tyuui: project (Q) -- "This story is a work of fiction."
    "tyuui": "本故事纯属虚构。",
    # tyuui@project_k: project_k (K) -- 3-line resemblance disclaimer
    "tyuui@project_k": "本故事纯属虚构。\\n如与实际存在的人物或组织\\n有所雷同，纯属巧合。",
    # tyuui2: project -- "June XXth, 1983"
    "tyuui2": "1983年6月XX日",

    # ---- Frederica Bernkastel chapter-opening poems -------------------------
    # si_onikakushi: project onik_op:12
    "si_onikakushi": "请别再苛责自己。\\n哪怕世界不肯原谅你，我也会原谅你。\\n\\n请别再苛责自己。\\n哪怕你不肯原谅这个世界，我也会原谅你。\\n\\n所以，请告诉我。\\n究竟要怎样，你才能原谅我呢？\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_watanagashi: project wata_001:13  (source card has the typo "truith")
    "si_watanagashi": "我不会为你解渴。\\n因为你追寻的真实，是你无法接受的。\\n\\n我不会为你解渴。\\n因为你渴望的真实，根本不存在。\\n\\n但我依然想为你解渴。\\n因为把你丢进这片荒漠的，正是我。\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_tatarigoroshi: project tata_001:13
    "si_tatarigoroshi": "井中之蛇过得很幸福。\\n因为它并不在意井外发生着什么。\\n\\n井中之蛇过得很幸福。\\n因为井外发生的事，与它毫无干系。\\n\\n而你也一样幸福。\\n因为你不知道井外发生着什么。\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_himatsubushi: project hima_001:26
    "si_himatsubushi": "你问，犯人是谁？\\n我们不是正在这个故事里寻找吗？\\n\\n你问，犯人是谁？\\n你可知道那个犯人做了什么？\\n\\n犯人是谁？\\n此刻将要杀死我的犯人，又是谁？！\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_meakasi: project_k meak_001:11
    "si_meakasi": "她把念珠掉在了沙地里。于是少女哭了。\\n此后一百年，少女翻遍了沙砾。\\n\\n也许掉进了海里，而不是沙地。于是少女哭了。\\n此后一百年，少女寻遍了海洋。\\n\\n也许掉进了山里，而不是海里。于是少女哭了。\\n还要再过多少年，少女才会想起去怀疑——自己是否真的弄丢过它们？\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_tumihorobosi: project_k tsum_op:16
    "si_tumihorobosi": "第一次，我会加倍努力，\\n去避开那无法避免的悲剧。\\n\\n第二次，我会对那无法避免的悲剧\\n感到厌恶。\\n\\n第三次，厌恶将化为煎熬。\\n到第七次，我大概已经笑得出来了。\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_minagorosi_1: project_k mina_op:961
    "si_minagorosi_1": "我想知道井外的世界。\\n于是我从井底拼命向上攀爬。\\n\\n我想知道井外的世界。\\n于是就算跌落受伤，我也继续攀爬。\\n\\n我终于发觉。\\n爬得越高，跌落时的伤痛就越深。\\n\\n当对世界的好奇与身体的疼痛不相上下之时……\\n我终于读懂了井底之蛙的含义。\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_minagorosi_2: project_k mina_022:12
    "si_minagorosi_2": "请告诉我，这一夜发生了什么。\\n这就像一只装着猫的箱子。\\n\\n请告诉我，这一夜发生了什么。\\n我甚至不知道，箱中的猫是生是死。\\n\\n请告诉我，这一夜发生了什么。\\n箱中之猫，已经死了。\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_maturibayasi_1: project_k mats_op:12 + mats_025:780
    "si_maturibayasi_1": "每个人都有获得幸福的资格。\\n难就难在承认这一点。\\n\\n每个人都有获得幸福的资格。\\n难就难在将它实现。\\n\\n我，也有获得幸福的资格。\\n难就难在找到一个折中之道。\\n\\n弗雷德里卡·伯恩卡斯特尔",
    # si_maturibayasi_2: project_k mats_025:782
    "si_maturibayasi_2": "因为从今往后，\\n我要活得远比过去幸福。\\n\\n我不会就此妥协。\\n我们错过的幸福，要统统取回来。\\n\\n我的一份是一百年，\\n你的一份是一千年。\\n\\n弗雷德里卡·伯恩卡斯特尔",

    # ---- Meakashi: Shion's notebook pages ----------------------------------
    # nort5: project_k meak_004:611
    "nort5": "我甚至不被允许在太阳底下自由行走。\\n在一个晴朗的日子，我遇见了一个男孩。\\n像我这样扭曲的女孩……\\n怎么会爱上他的纯真呢？\\n\\n笔记本 第5页",
    # nort19: project_k meak_007:10
    "nort19": "有些日子能见到他，有些日子见不到。\\n晴空会转阴，雨也终会停歇。\\n我以为他的不在也是如此。\\n可他其实已濒临崩溃。\\n\\n笔记本 第19页",
    # nort26: project_k meak_008:1156
    "nort26": "我对自己这份孩子气感到厌恶。\\n我只是想填补内心的空洞，根本没有在乎过他。\\n相比之下，悟史君真是非常宽容。\\n可是……我能不能原谅沙都子，就另当别论了。\\n\\n笔记本 第26页",
    # nort27: project_k meak_011:872
    "nort27": "只要亮出我真正的身份，我就能救悟史君。\\n我很清楚这有多危险。\\n一旦暴露，祖母一定会把我抓回去。\\n但我没有想过那之后会如何。\\n\\n笔记本 第27页",
    # nort43: project_k meak_014:686
    "nort43": "悟史君消失了。\\n不仅如此，连他消失的理由也一同消失了。\\n这一定是人干的事。\\n我无法接受他是被鬼隐了。\\n\\n笔记本 第43页",
    # nort150: project_k meak_015:1065
    "nort150": "这本笔记本，我已经许久没有翻开了。\\n我的心情已经写满了150多页。\\n这本笔记本，就是我内心的钥匙。\\n从去年起就一直在沉睡的另一个我\\n正在缓缓苏醒……\\n\\n笔记本 第150页",
    # nort159: project_k meak_016:168
    "nort159": "和他在一起的日子，我从不厌倦。\\n他真的很可爱哦？\\n我们总是走在一起。\\n可每当我停下脚步，他总会多走出一步。\\n那样子太惹人怜爱了。我爱极了！\\n\\n笔记本 第159页",
    # nort165: project_k meak_017:113
    "nort165": "另一个我告诉过我。\\n说我正身处魔物的胃袋之中。\\n如果没有听见那个声音，我本不会醒来。\\n说不定，就那样永远不会醒来了。\\n\\n笔记本 第165页",
    # nort186: project_k meak_019:977
    "nort186": "谁也无法分辨我们。\\n我们是魅音和诗音，完美的双生子。\\n\\n笔记本 第186页",

    # ---- Meakashi epilogue (white background pages) ------------------------
    # meaed1: project_k meakashi_epilogue:591
    "meaed1": "我曾无数次希望，这一切只是一场梦。\\n\\n于是，我把它写了下来，\\n盼望着它能成真。",
    # meaed2: project_k meakashi_epilogue:597
    "meaed2": "漫画里的梦，常常是这样的。\\n\\n“眼前堆着小山一样的点心！根本吃不完嘛”\\n我伸手去够，\\n却在这时被谁叫醒了。",
    # meaed3: project_k meakashi_epilogue:605
    "meaed3": "这场梦，实在是太漫长了。\\n我一定已经睡了不止一年。",
    # meaed4: project_k meakashi_epilogue:609
    "meaed4": "啊，对了。\\n我逃掉了棒球练习。\\n在红灯的时候踏上了马路，\\n被摩托车撞了。\\n\\n从那以后我一直昏迷不醒，直到今天终于醒了过来。",
    # meaed5: project_k meakashi_epilogue:619
    "meaed5": "睁开眼睛，我看到的是医院的天花板。\\n\\n悟史君在床边看着我……\\n\\n啊哈哈哈。这未免也太完美了。",
    # meaed6: project_k meakashi_epilogue:627
    "meaed6": "不过，这样也好，对吧？\\n\\n就这样收场，也可以吧？",
    # meaed7: project_k meakashi_epilogue:635 (text at bottom right)
    "meaed7": "对不起……生下了我。",

    # ---- Minagoroshi: Rika's fragment narration (white background) ---------
    # mina_katari1: project_k mina_020:439
    "mina_katari1": "在我们四处奔跑嬉闹的时候，\\n许多人开始主动亲近沙都子。\\n\\n有人关切她的伤势，\\n有人同情她一直以来的遭遇，\\n还有人一口保证，她有事随时可以找他们。",
    # mina_katari2: project_k mina_020:441
    "mina_katari2": "而这一切，\\n对还不习惯这些的沙都子来说，\\n一定新鲜得让人不知所措。\\n\\n沙都子说，这些反常的温柔\\n反而让她浑身不自在，\\n可我知道，她只是在害羞罢了。\\n正是这些，才让沙都子\\n真切地感到村子已经重获新生。",
    # mina_katari3: project_k mina_020:507
    "mina_katari3": "赤坂到来之时，我曾以为，改变命运\\n靠的是某个有影响力的大人物。\\n至少当时我是这么想的。\\n\\n但事实证明，那不过是个误会。",
    # mina_katari4: project_k mina_020:509
    "mina_katari4": "奇迹不是个人创造的。\\n必须人人都站出来，奇迹才会发生。\\n所以，当我以为只要有赤坂在身边\\n就能战胜命运的时候——\\n那全是我的一厢情愿。\\n\\n就算他当时真的在我身边，\\n我们恐怕也什么都做不成，\\n只会白白让自己失望而已。",
    # mina_katari5: project_k mina_020:511
    "mina_katari5": "我并不是说赤坂有什么错——\\n根本不是那么回事。\\n或许我心里曾骂过他是个“废物”。\\n……连我自己都对自己嘴巴之毒感到吃惊。\\n\\n今晚就别提这些了。\\n都几十年没见了，不如为我们的重逢庆祝一番？",
    # mina_katari6: project_k mina_020:568  (source card has the typo "coucil")
    "mina_katari6": "圭一也备受瞩目，走到哪里都是焦点。\\n\\n为了拯救沙都子，他挺身而出，\\n他的领导才能从此传遍了全村。\\n何况，他成功说动村议会、乃至园崎魉本人，\\n这些如今都已成了传颂他英名的传奇故事。",
    # mina_katari7: project_k mina_020:570
    "mina_katari7": "所有人都已经明白，\\n沙都子曾遭到全村的排挤。\\n\\n他们也明白那是多么不讲道理，\\n大坝战争早已落幕，欺凌却迟迟未散。\\n圭一奋力冲破那道禁忌的身影是如此痛快，\\n让人窥见了村子崭新的未来，\\n他的英勇之举也赢得了老老少少的一致称赞。",
    # mina_katari8: project_k mina_020:573  (source card has the typo "unprecedent")
    "mina_katari8": "话虽如此，如今前原圭一已经成了\\n雏见泽村民们热议的话题。\\n大家自然都想一睹这位前原圭一的风采，\\n于是那场廉价拍卖会\\n迎来了空前的人潮。",
    # mina_katari9: project_k mina_020:575
    "mina_katari9": "虽然他一开始涨红了脸，\\n可一旦克服了羞涩，圭一便显出了真本事。\\n他以十足的干劲和气势引得人群欢呼雀跃，\\n令那一年的昭和58年绵流祭\\n呈现出前所未见的热烈气氛。\\n\\n如今，圭一赢得了全村人的敬佩与认可。",
    # mina_katari10: project_k mina_020:577
    "mina_katari10": "我相信，即使在此之后，圭一也会\\n继续引领村子迎接新的冒险。\\n\\n出现了这样一位年轻的领头人，\\n村里的长老们\\n也相当安心。",
    # mina_katari11: project_k mina_020:640
    "mina_katari11": "回到主帐中的，是最后才赶来的\\n园崎家一群举足轻重的人物。\\n\\n他们正是我们昨天欠下人情的那些人。\\n除了沙都子，所有人都低下了头。\\n就在几天之前，在场的每一个人\\n都还可能是坐下来喝酒时\\n数落北条家不是的人。",
    # mina_katari12: project_k mina_020:642  (source card has the typo "jn")
    "mina_katari12": "但圭一冲破了这一切。\\n这些人对自己的冷漠薄情作过反省，\\n我想他们当中不会再有人\\n歧视沙都子了。\\n\\n事实上，他们纷纷低头，\\n为自己先前的所作所为道歉，并许诺\\n日后若有什么事，定当鼎力相助。",
    # mina_katari13: project_k mina_020:719
    "mina_katari13": "圭一的父母也来了祭典。\\n他们被大家围了个水泄不通——\\n都夸他们“养了这么出色的儿子”，\\n是今日大英雄的父母。\\n\\n据圭一说，他父母平日忙得很少出门，\\n这次正好是个和村民们多多交流的好机会。",
    # mina_katari14: project_k mina_020:721
    "mina_katari14": "圭一的父亲还自豪地自告奋勇，\\n说镇议会若有需要，海报尽管交给他。\\n\\n……听圭一说，他父亲画的海报\\n好到甚至会被人揭走。\\n\\n真让人期待，那到底是怎样的海报。",
    # mina_katari15: project_k mina_020:781
    "mina_katari15": "我听见羽入难以置信地低声说着，\\n就在不久之前，还有这样一个世界——\\n诗音把沙都子折磨至死。\\n\\n那个恐怖的世界，\\n这个迎来幸福结局的世界，\\n都是同一个雏见泽。",
    # mina_katari16: project_k mina_020:783
    "mina_katari16": "我敢肯定，只知晓这个世界的我们\\n会坚定不移地相信，雏见泽注定\\n会迎来幸福的结局。\\n\\n只有我和羽入知道。\\n只有旁观者知道。\\n在这个雏见泽，只隔着一层薄得\\n比捞金鱼的纸网还要薄的膜——\\n那里还有无数个迎来悲惨结局的世界。",
    # mina_katari17: project_k mina_020:785
    "mina_katari17": "正因如此，\\n我确信我们比任何人都明白\\n这个世界是多么值得庆幸。\\n\\n如果圭一他们任由怒火驱使，\\n不肯并肩而战，\\n就不会有今天这一天。",
    # mina_katari18: project_k mina_020:787
    "mina_katari18": "如果圭一没能压住怒火，他今天就会\\n铸成大罪。\\n诗音也一样。她今天就会成为罪犯。\\n换成蕾娜的话，她恐怕早已抢先三步\\n连善后都料理完了。\\n\\n……只有魅音从未爆发过。\\n那算是沉稳还是怯懦，我也说不准，\\n……哎呀，这话可不该说。",
    # mina_katari19: project_k mina_020:789
    "mina_katari19": "当然，实际上也确实有过我失控的世界。\\n……最后把自己搭了进去。真没出息。\\n\\n总之，那些世界没有一个有好下场。\\n我们始终没能夺回属于我们的幸福日常。",
    # mina_katari20: project_k mina_020:791
    "mina_katari20": "所以，我曾放弃过希望。\\n但其他人谁都没有放弃。\\n我们万众一心，去促成\\n那场必须发生的奇迹。\\n\\n奇迹发生了，因为所有人齐心协力。",
    # mina_katari21: project_k mina_020:793
    "mina_katari21": "这么说也许显得自吹自擂\\n……但我认为，哪怕只有我一个人放弃、否认齐心，\\n奇迹也不会发生。\\n\\n在最后那通电话里，如果我没有\\n从圭一手中夺下听筒，\\n我想沙都子就不会开口向我们求助。",
    # mina_katari22: project_k mina_020:795
    "mina_katari22": "就是这样。那场若非所有人齐聚一心\\n便绝无可能发生的奇迹。\\n那场只要我们之中有一人放弃\\n便不会存在的奇迹。\\n\\n多亏了圭一\\n让我明白，突破命运原来如此简单。\\n而那个一开始就放弃了的我。",
    # mina_katari23: project_k mina_020:797
    "mina_katari23": "如果一切都是命运，\\n如果圭一的存在自有其意义，\\n那它究竟想告诉我什么？\\n\\n我早已知道答案。\\n那就是抗争命运的意义，以及战斗的方法。\\n\\n我绝不会再向命运低头。一次也不会。",
    # mina_katari24: project_k mina_020:799
    "mina_katari24": "这与羽入对我的告诫恰好相反——\\n她说不要对任何事抱有期待。\\n\\n就连羽入，只要不放弃地去相信，\\n也一定能引发某种奇迹。\\n我试着这样劝她，可她偏偏在最要紧的时候犯倔，\\n只用一句“啊呜啊呜”就把我应付了过去。",

    # ---- Minagoroshi epilogue: Takano's monologue (white background) -------
    # takano_1: project_k mina_ep:1117
    "takano_1": "如今，我的理想已经圆满。\\n这里正是名副其实的乌托邦。\\n在这里，我就是神，\\n铭刻于此的作祟将永远流传下去。",
    # takano_2: project_k mina_ep:1182
    "takano_2": "托大坝战争的福，一位神明从长眠中苏醒，\\n在绵流祭的神圣之夜降罚于不信之人。\\n年复一年，那位神明不断苏醒。\\n伟大的御社神大人醒来了。\\n于是，他们退回了面对作祟时那份原始的恐惧。",
    # takano_3: project_k mina_ep:1215
    "takano_3": "没有人再怀疑御社神大人的作祟，\\n它已从尸骸的腹中完美复苏。\\n如今，复活降世。\\n当你触怒御社神大人之时，\\n地狱的鼎镬便会迸裂横溢，\\n逃亡之人将咽下最后一口气。\\n伴随那最终的审判，作祟终于成真！",
    # takano_4: project_k mina_ep:1235
    "takano_4": "当你死去，还能留下什么？\\n肉体将腐烂至白骨，碾作尘沙。\\n除了化作大地的肥料，你还能留下什么？",
    # takano_5: project_k mina_ep:1343
    "takano_5": "我会留存下来。\\n一个名字，一桩伟业，一份留下的作祟。\\n我的存在将在这片土地上被永远奉为神明。\\n而从今日的作祟中逃生的人，将对此心怀敬畏。\\n他们会把这份恐惧传给他人。\\n那群人的记忆，\\n终将升华为我——而我，将超越一切。",
    # takano_6: project_k mina_ep:1615
    "takano_6": "我就是御社神大人。\\n这就是御社神大人的作祟。\\n他们将崇拜我、奉我为神，并畏惧我。\\n当我出手，他们便会祈求不要作祟、不要死亡。\\n我的事业将成为历史。\\n我的存在与这份作祟的历史，将被传颂万代。",
    # takano_7: project_k mina_ep:1628
    "takano_7": "我已超越血肉之躯，化作了作祟本身。\\n即使这具躯壳腐朽，\\n我的事业也将永载史册\\n\\n如今，我已获得永生。",
    # takano_8: project_k mina_ep:1635
    "takano_8": "人类啊，血肉便是你们的诅咒。\\n当肉体腐朽，你们什么也留不下。\\n你们的恶意、悔恨与恐惧。\\n而你们终将明白我的伟大。\\n我已成为御社神大人。\\n如今，我已踏入神之领域。\\n即使这具身体被毁，我在此的所作所为也将永远流传。\\n我已得到永恒的生命。",

    # ---- Matsuribayashi: fight / dramatic flash-cards ----------------------
    # ma_1: project_k mats_021:3430 -- Okonogi boasts
    "ma_1": "我可是山狗的小木！！",
    # ma_2: project_k mats_021:3434 -- Akasaka's dry retort
    "ma_2": "那可真是了不起呢。",
    # ma_3: project_k mats_021:3439 -- Akasaka's taunt (white bg card)
    "ma_3": "那么说，他们给了你多少钱，嗯？",
    # maturi_txt1: project_k mats_021:2768
    "maturi_txt1": "……赶上了……",
    # maturi_txt2: project_k mats_021:2813
    "maturi_txt2": "梨花酱",
    # maturi_txt2b: project_k mats_021:2816
    "maturi_txt2b": "我来",
    # maturi_txt2c: project_k mats_021:2820 (Shake)
    "maturi_txt2c": "救你了！",
    # maturi_txt3: project_k mats_021:2969
    "maturi_txt3": "赤坂火力全开",
    # maturi_txt3b: project_k mats_021:2972
    "maturi_txt3b": "从第一枪起！",
    # maturi_txt4: project_k mats_021:2976
    "maturi_txt4": "所以他只需要一发。",
    # maturi_txt5: project_k mats_021:2981 (Shake)
    "maturi_txt5": "他毫不留情！！",
    # maturi_txt6: project_k mats_021:3004
    "maturi_txt6": "他的力量，宛如",
    # maturi_txt6b: project_k mats_021:3009 (white bg)
    "maturi_txt6b": "装甲\\n贯穿\\n弹药。",
    # maturi_txt6c: project_k mats_021:3010 (white bg, shadow variant of 6b)
    "maturi_txt6c": "装甲\\n贯穿\\n弹药。",
    # maturi_txt7: project_k mats_021:3224 & 3242
    "maturi_txt7": "……太轻了。",
    # maturi_txt9: project_k mats_022:3358 (white bg; flashes together with txt10)
    "maturi_txt9": "在",
    # maturi_txt10: project_k mats_022:3360 (white bg, shadow)
    "maturi_txt10": "天堂",
    # maturi_txt10b: project_k mats_022:3361 (white bg)
    "maturi_txt10b": "天堂",
    # maturi_txt11: project_k mats_024:2580 -- Takano on Rika
    "maturi_txt11": "怪物",
    # maturi_txt13: project_k mats_011:846 -- Takano on Rika
    "maturi_txt13": "怪物",

    # ---- Matsuribayashi epilogue (white background card) -------------------
    # okaerinasai: project_k mats_024:2761
    "okaerinasai": "欢迎回家，妈妈。",

    # ---- Chapter number cards (white bg, red text) --------------------------
    # title_mea_j / title_mea: project_k meak_001:47 / :49
    "title_mea_j": "第五章 目明篇",
    "title_mea": "第五章 目明篇",
    # title_tsumi_j / title_tsumi: project_k tsum_op:54 / :56
    "title_tsumi_j": "第六章 罪灭篇",
    "title_tsumi": "第六章 罪灭篇",
    # title_mina_j / title_mina: project_k mina_op:1001 / :1003
    "title_mina_j": "第七章 皆杀篇",
    "title_mina": "第七章 皆杀篇",
}
