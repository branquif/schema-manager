let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Dropbox/swf_projects/schema-manager
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +25 tests/schemas/type_test.schm
badd +39 grammar/scheman_pure.lark
badd +1 grammar/elements.py
badd +1 grammar/data_types.py
badd +243 grammar/scheman_parser.py
argglobal
silent! argdel *
edit grammar/scheman_parser.py
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
exe 'vert 1resize ' . ((&columns * 99 + 100) / 200)
exe '2resize ' . ((&lines * 38 + 41) / 83)
exe 'vert 2resize ' . ((&columns * 100 + 100) / 200)
exe '3resize ' . ((&lines * 40 + 41) / 83)
exe 'vert 3resize ' . ((&columns * 100 + 100) / 200)
argglobal
let s:l = 121 - ((73 * winheight(0) + 39) / 79)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
121
normal! 039|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm') | buffer ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | else | edit ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm | endif
let s:l = 118 - ((3 * winheight(0) + 19) / 38)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
118
normal! 017|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman_pure.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman_pure.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman_pure.lark | endif
let s:l = 120 - ((5 * winheight(0) + 20) / 40)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
120
normal! 071|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 99 + 100) / 200)
exe '2resize ' . ((&lines * 38 + 41) / 83)
exe 'vert 2resize ' . ((&columns * 100 + 100) / 200)
exe '3resize ' . ((&lines * 40 + 41) / 83)
exe 'vert 3resize ' . ((&columns * 100 + 100) / 200)
tabedit ~/Dropbox/swf_projects/schema-manager/grammar/data_types.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 100 + 100) / 200)
exe 'vert 2resize ' . ((&columns * 99 + 100) / 200)
argglobal
let s:l = 51 - ((48 * winheight(0) + 39) / 79)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
51
normal! 024|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/elements.py') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/elements.py | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/elements.py | endif
let s:l = 145 - ((32 * winheight(0) + 39) / 79)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
145
normal! 018|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
exe 'vert 1resize ' . ((&columns * 100 + 100) / 200)
exe 'vert 2resize ' . ((&columns * 99 + 100) / 200)
tabnext 1
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
