let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Dropbox/swf_projects/schema-manager
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +19 grammar/scheman.lark
argglobal
silent! argdel *
edit grammar/scheman.lark
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 39 + 41) / 83)
exe '2resize ' . ((&lines * 39 + 41) / 83)
argglobal
let s:l = 59 - ((22 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
59
normal! 024|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
argglobal
if bufexists('~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark') | buffer ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | else | edit ~/Dropbox/swf_projects/schema-manager/grammar/scheman.lark | endif
let s:l = 206 - ((18 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
206
normal! 057|
lcd ~/Dropbox/swf_projects/schema-manager
wincmd w
exe '1resize ' . ((&lines * 39 + 41) / 83)
exe '2resize ' . ((&lines * 39 + 41) / 83)
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
