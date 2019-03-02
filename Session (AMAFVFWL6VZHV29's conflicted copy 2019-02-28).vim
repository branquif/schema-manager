let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Dropbox/swf_projects/schema-manager
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +192 grammar/scheman_parser.py
badd +13 grammar/scheman_pure.lark
badd +1 tests/schemas/type_test.schm
badd +1 grammar/scheman_types.py
argglobal
silent! argdel *
edit grammar/scheman_parser.py
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
exe '1resize ' . ((&lines * 21 + 24) / 48)
exe 'vert 1resize ' . ((&columns * 82 + 89) / 178)
exe '2resize ' . ((&lines * 22 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 82 + 89) / 178)
exe 'vert 3resize ' . ((&columns * 95 + 89) / 178)
argglobal
let s:l = 141 - ((14 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
141
normal! 014|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman_parser.py') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman_parser.py | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman_parser.py | endif
let s:l = 201 - ((10 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
201
normal! 015|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman_pure.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman_pure.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman_pure.lark | endif
let s:l = 74 - ((22 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
74
let s:c = 53 - ((33 * winwidth(0) + 47) / 95)
if s:c > 0
  exe 'normal! ' . s:c . '|zs' . 53 . '|'
else
  normal! 053|
endif
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 21 + 24) / 48)
exe 'vert 1resize ' . ((&columns * 82 + 89) / 178)
exe '2resize ' . ((&lines * 22 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 82 + 89) / 178)
exe 'vert 3resize ' . ((&columns * 95 + 89) / 178)
tabedit ~/Dropbox/swf_projects/schema-manager/tests/schemas/type_test.schm
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
let s:l = 7 - ((6 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 011|
lcd ~/Dropbox/swf_projects/schema-manager
tabedit ~/Dropbox/swf_projects/schema-manager/grammar/scheman_types.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
let s:l = 35 - ((34 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
35
normal! 018|
lcd ~/Dropbox/swf_projects/schema-manager
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
