



text = f"""
#-- Welcome to nics settings
#----------------------------

#-- Everything starts with "#--" is a comment.



author: 'Nicholas Valentinus'


#-- Colors

hue_signature: 22


lowercase_the_url: True
show_credit: True



#-- Help
#-----------------------------------
#--
#-- Inside this folder (the folder that contains this setting.txt file),
#-- nics will strictly look at the following things:
#--    (optional) assets/ . . : the folder for storing items used in markdown files
#--    (REQUIRED) tree/ . . . : the docs structure
#--    (optional) 404.md  . . : 404 page
#--    (optional) favicon.png : currently, only PNG format is supported
#--    (REQUIRED) settings.txt: the main settings
#-- And nics will not touch any other files/folders that are being added to this folder
#--
#--
#-- Inside tree/ folder, 
#-- 
#-- 
#-- If you find this help outdated, you can visit https://nvfp.github.io/now-i-can-sleep/guide to read the latest guidelines.



#-- == internal == 
#-- (please do not modify any of these)

_nics_version: '1.0.0'

_docs: r'docs'
_target: r'docs'

_coloring_type: 'signature'

_copyright_style: 'default'

_git_push_name: 'NICS'
_git_push_email: '0@gmail.com'
"""