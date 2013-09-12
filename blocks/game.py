__author__ = 'Kevin'
import universe
import render
import multiprocessing



def play_game(i, name):
    game = universe.Universe(i, name)
    game.play_loop()
    print "game process ending."
    return True

def renderer(i, name):
    ren = render.Renderer(i,name)
    ren.render_loop()
    print "render process ending."
    return True



universepipe, renderpipe = multiprocessing.Pipe()

universe_process = multiprocessing.Process(
    target=play_game,
    args=(universepipe, "universe",)
)
universe_process.start()

rendering_process = multiprocessing.Process(
    target=renderer,
    args=(renderpipe, 'renderer')
)
rendering_process.start()

rendering_process.join()
renderpipe.recv()
universe_process.join()