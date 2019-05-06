let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Dropbox/swf_projects/schema-manager
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +8 tests/schemas/type_test.schm
badd +59 scheman/elements.py
badd +16 scheman/data_types.py
badd +93 scheman/type_parser.py
badd +13 grammar/scheman.lark
badd +35 scheman/record_parser.py
badd +63 docs/scheman_model.uml
badd +1 examples/mapping.schm
badd +1 tasks.py
badd +19 scheman/common_parser.py
argglobal
silent! argdel *
edit grammar/scheman.lark
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 129 - ((41 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
129
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
tabedit ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 202 - ((35 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
202
normal! 011|
lcd ~/Dropbox/swf_projects/schema-manager
tabedit ~/Dropbox/swf_projects/schema-manager/scheman/common_parser.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 1resize ' . ((&columns * 147 + 99) / 198)
exe '2resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 147 + 99) / 198)
exe 'vert 3resize ' . ((&columns * 50 + 99) / 198)
argglobal
setlocal fdm=expr
setlocal fde=SimpylFold#FoldExpr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=2
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 19 - ((9 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm') | buffer ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | else | edit ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 22 - ((8 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 30 - ((15 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
normal! 028|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
exe '1resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 1resize ' . ((&columns * 147 + 99) / 198)
exe '2resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 147 + 99) / 198)
exe 'vert 3resize ' . ((&columns * 50 + 99) / 198)
tabedit ~/Dropbox/swf_projects/schema-manager/scheman/type_parser.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 147 + 99) / 198)
exe '2resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 50 + 99) / 198)
exe '3resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 50 + 99) / 198)
argglobal
setlocal fdm=expr
setlocal fde=SimpylFold#FoldExpr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 93 - ((92 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
93
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 92 - ((13 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
92
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm') | buffer ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | else | edit ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 35 - ((11 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
35
normal! 041|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
exe 'vert 1resize ' . ((&columns * 147 + 99) / 198)
exe '2resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 50 + 99) / 198)
exe '3resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 50 + 99) / 198)
tabedit ~/Dropbox/swf_projects/schema-manager/scheman/record_parser.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 147 + 99) / 198)
exe '2resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 50 + 99) / 198)
exe '3resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 50 + 99) / 198)
argglobal
setlocal fdm=expr
setlocal fde=SimpylFold#FoldExpr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=2
setlocal fml=1
setlocal fdn=20
setlocal fen
21
normal! zo
let s:l = 35 - ((25 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
35
normal! 02|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm') | buffer ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | else | edit ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 170 - ((16 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
170
normal! 020|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 108 - ((6 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
108
normal! 027|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
exe 'vert 1resize ' . ((&columns * 147 + 99) / 198)
exe '2resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 50 + 99) / 198)
exe '3resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 50 + 99) / 198)
tabedit ~/Dropbox/swf_projects/schema-manager/scheman/data_types.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 114 + 99) / 198)
exe '2resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 83 + 99) / 198)
exe '3resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 83 + 99) / 198)
argglobal
setlocal fdm=expr
setlocal fde=SimpylFold#FoldExpr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=2
setlocal fml=1
setlocal fdn=20
setlocal fen
15
normal! zo
113
normal! zo
143
normal! zo
152
normal! zo
166
normal! zo
203
normal! zo
230
normal! zo
448
normal! zo
let s:l = 16 - ((15 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 31 - ((15 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
let s:c = 49 - ((42 * winwidth(0) + 41) / 83)
if s:c > 0
  exe 'normal! ' . s:c . '|zs' . 49 . '|'
else
  normal! 049|
endif
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/scheman/elements.py') | buffer ~/Dropbox/swf_projects/schema-manager/scheman/elements.py | else | edit ~/Dropbox/swf_projects/schema-manager/scheman/elements.py | endif
setlocal fdm=expr
setlocal fde=SimpylFold#FoldExpr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=2
setlocal fml=1
setlocal fdn=20
setlocal fen
37
normal! zo
38
normal! zc
37
normal! zc
55
normal! zo
130
normal! zo
130
normal! zc
147
normal! zo
147
normal! zc
160
normal! zo
160
normal! zc
186
normal! zo
186
normal! zc
208
normal! zo
208
normal! zc
221
normal! zo
221
normal! zc
271
normal! zo
271
normal! zc
288
normal! zo
288
normal! zc
let s:l = 56 - ((30 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
56
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
exe 'vert 1resize ' . ((&columns * 114 + 99) / 198)
exe '2resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 83 + 99) / 198)
exe '3resize ' . ((&lines * 23 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 83 + 99) / 198)
tabedit ~/Dropbox/swf_projects/schema-manager/docs/scheman_model.uml
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 5 - ((4 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 0
lcd ~/Dropbox/swf_projects/schema-manager
tabedit ~/Dropbox/swf_projects/schema-manager/tasks.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=expr
setlocal fde=SimpylFold#FoldExpr(v:lnum)
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=1
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 3 - ((2 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 02|
lcd ~/Dropbox/swf_projects/schema-manager
tabedit ~/Dropbox/swf_projects/schema-manager/examples/mapping.schm
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 28 - ((27 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
normal! 017|
lcd ~/Dropbox/swf_projects/schema-manager
tabnext 7
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=30 winminheight=1 winminwidth=1 shortmess=aoOTIcF
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
let g:this_session = v:this_session
let g:this_obsession = v:this_session
let g:this_obsession_status = 2
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
