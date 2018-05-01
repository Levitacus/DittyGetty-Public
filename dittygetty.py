import click

@click.group()
def entry_point():
    '''entry point to the cli'''
    pass #entry point to the cli

@entry_point.group()
def playlist():
    '''test'''
    pass
    
@playlist.group('modify')
def playlist_modify():
    pass
    
@playlist_modify.command('add')
@click.argument('song')
@click.argument('artist')
@click.pass_obj
def playlist_add(song, artist):
    '''Adds a song to the current playlist'''
    click.echo('Song: %s. Artist: %s. \n' %(song, artist))
    
entry_point.add_command(playlist)

if __name__ == '__main__':
    entry_point()
    
#So this creates a chain of commands.
#You can do 
#python dittygetty.py playlist modify add "21st Century Schizoid Man" "King Crimson"
#and it works