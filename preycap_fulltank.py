import os
import sys
from pandac.PandaModules import WindowProperties
import pandac.PandaModules
# from panda3d.core import Shader
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import numpy as np
from scipy.ndimage.filters import gaussian_filter

pandac.PandaModules.loadPrcFileData("", """
            fullscreen 0
            load-display pandagl
            win-origin 0 0
            undecorated 0
            win-size 640 400
            sync-video 1
            """)

# pandac.PandaModules.loadPrcFileData("", """
#             fullscreen 1
#             load-display pandagl
#             win-origin 0 0
#             undecorated 1
#             win-size 2560 1600
#             sync-video 1
#             """)


class MyApp(ShowBase):
    def __init__(self):
        homedir = '/Users/nightcrawler2/PreycapMaster/'
        sim_text = raw_input('Simulation Type: ')
        if sim_text == 's':
            simulation = True
        if sim_text == 'r' or sim_text == 't':
            simulation = False
        if not simulation:
            if sim_text == 't':
                para_cont_window = np.load(
                    homedir + 'para_continuity_window.npy')
                para_cont_window = int(para_cont_window)
            else:
                para_cont_window = 0
            para_positions = np.load(
                homedir + '3D_paracoords.npy')[:, para_cont_window:]
            fish_position = np.load(homedir + 'ufish_origin.npy')
            fish_orientation = np.load(homedir + 'ufish.npy')
            try:
                self.strikelist = np.load(homedir + 'strike.npy')
            except IOError:
                self.strikelist = np.zeros(fish_position.shape[0])
        elif simulation:
            para_positions = np.load(
                homedir + 'para_simulation.npy')
            fish_position = np.load(
                homedir + 'origin_model.npy')
            fish_orientation = np.load(
                homedir + 'uf_model.npy')
            if para_positions.shape[1] != fish_position.shape[0]:
                end_fp = [fish_position[-1] for i in range(
                    para_positions.shape[1]-fish_position.shape[0])]
                end_fo = [fish_orientation[-1] for i in range(
                    para_positions.shape[1]-fish_orientation.shape[0])]
                fish_position = np.concatenate((fish_position, end_fp))
                fish_orientation = np.concatenate((fish_orientation, end_fo))
            try:
                self.strikelist = np.load(
                    homedir + 'strike.npy')
                print self.strikelist.shape
            except IOError:
                self.strikelist = np.zeros(fish_position.shape[0])
                print self.strikelist.shape

        else:
            self.exitmodel()
        self.numpara = para_positions.shape[0]
        self.numframes = para_positions.shape[1]
        self.para_positions = para_positions

        dfx = gaussian_filter([x[0] for x in fish_position], 1)
        dfy = gaussian_filter([y[1] for y in fish_position], 1)
        dfz = gaussian_filter([z[2] for z in fish_position], 1)
        fish_position_filt = np.array(
            [[x, y, z] for x, y, z in zip(dfx, dfy, dfz)])
        self.fish_position = fish_position_filt
        
        fox = gaussian_filter([x[0] for x in fish_orientation], 1)
        foy = gaussian_filter([y[1] for y in fish_orientation], 1)
        foz = gaussian_filter([z[2] for z in fish_orientation], 1)
        fish_orientation_filt = np.array(
            [[x, y, z] for x, y, z in zip(fox, foy, foz)])
        self.fish_orientation = fish_orientation_filt

        print fish_orientation.shape
        print fish_position.shape
        print para_positions.shape

        print('numframes')
        print self.numframes
        ShowBase.__init__(self)
        self.accept("escape", self.exitmodel)
#        self.accept("escape", sys.exit)
        props = WindowProperties()
        props.setCursorHidden(False)
        props.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(props)
        self.lens1 = pandac.PandaModules.PerspectiveLens()
        self.lens1.setFov(90, 90)
        self.lens1.setNearFar(.1, 10000)
#        self.lens1.setAspectRatio(1920/1080.)
        self.lens1.setAspectRatio(1280/800.)
        self.cam.node().setLens(self.lens1)
        pivot = render.attachNewNode("pivot")
#        pivot.setPos(-1200, -1200, 944)
        pivot.setPos(3000, 3000, 944)
        self.cam.reparentTo(pivot)
#        self.cam.setH(100)

#        self.cam.setPos(-450, 944, 944)
        self.setBackgroundColor(1, 1, 1, 1)

        # Some Lines That Define Tank Boundaries
        self.d2 = pandac.PandaModules.LineSegs()
        self.d2.setColor(.5, .5, .5, 1)
        self.d2.setThickness(2)
        self.d2.moveTo(0, 0, 0)
        self.d2.drawTo(1888, 0, 0)
        self.d2.moveTo(0, 0, 0)
        self.d2.drawTo(0, 0, 1888)
        self.d2.moveTo(0, 0, 0)
        self.d2.drawTo(0, 1888, 0)
        self.d2.moveTo(1888, 1888, 0)
        self.d2.drawTo(1888, 1888, 1888)
        self.d2.moveTo(0, 1888, 1888)
        self.d2.drawTo(1888, 1888, 1888)
        self.d2.moveTo(1888, 0, 1888)
        self.d2.drawTo(1888, 1888, 1888)
        self.d2.moveTo(1888, 0, 0)
        self.d2.drawTo(1888, 1888, 0)
        self.d2.moveTo(1888, 0, 0)
        self.d2.drawTo(1888, 0, 1888)
        self.d2.moveTo(0, 1888, 0)
        self.d2.drawTo(1888, 1888, 0)
        self.d2.moveTo(0, 1888, 0)
        self.d2.drawTo(0, 1888, 1888)
        self.d2.moveTo(0, 0, 1888)
        self.d2.drawTo(0, 1888, 1888)
        self.d2.moveTo(0, 0, 1888)
        self.d2.drawTo(1888, 0, 1888)
        self.reference = self.loader.loadModel("sphere-highpoly")
        self.reference.reparentTo(self.render)
        self.reference.setScale(.01, .01, .01)
        self.reference.setColor(1, 1, 1)
        self.reference.setPos(944, 944, 944)
        self.cam.lookAt(self.reference)

        drawtank = True
        scale = 1888
        if drawtank:
            self.tank = self.loader.loadModel("rgbCube.egg")
            self.tank.reparentTo(self.render)
            self.tank.setScale(scale, scale, scale)
            self.tank.setTransparency(1)
            self.tank.setAlphaScale(0.2)
            self.tank.setColor(.3, .6, .9)
            self.tank.setPos(scale / 2, scale / 2, scale / 2)


# #
        geom2 = self.d2.create()
        self.nodegeom2 = self.render.attachNewNode(geom2)
        # Load the environment model.

        self.fishcone = self.loader.loadModel("Spotlight.egg")
        self.fishcone.setTexture(self.loader.loadTexture("white.png"), 1)
        self.fishcone.reparentTo(self.render)
        self.fishcone.setPos(0, 0, 0)
        self.fishcone.setScale(10, 10, 10)
        self.fishcone.setTransparency(1)
        self.fishcone.setAlphaScale(.5)
        self.fishcone.setColor(0, 0, 1)
        ''' These three lines make sure this is drawn before the tank.
        If you don't do this, tank blocks out the fishcone.'''
        self.fishcone.setBin("fixed", 0)
        self.fishcone.setDepthTest(False)
        self.fishcone.setDepthWrite(False)

        self.fishcone.show()

        self.spheres = dict({})
        for i in range(int(self.numpara/3)):
            self.spheres[i] = self.loader.loadModel("sphere.egg")
            # self.spheres[i] = Actor("models/panda-model",
            #                 {"walk": "models/panda-walk4"})
            self.spheres[i].reparentTo(self.render)
            self.spheres[i].setScale(15, 15, 15)
            self.spheres[i].setColor(.25, .25, .25)
            # text = pandac.PandaModules.TextNode('node name')
            # text.setText(' ' + str(i))
            # textNodePath = self.spheres[i].attachNewNode(text)
            # textNodePath.setScale(10)
            # textNodePath.setTwoSided(True)
            # textNodePath.setPos(-10, 0, 0)
            # textNodePath.setHpr(180, 0, 0)

#        self.sphere_fish = self.loader.loadModel("sphere-highpoly.egg")
        self.sphere_fish = self.loader.loadModel("sphere.egg")
        self.sphere_fish.reparentTo(self.render)
        self.sphere_fish.setScale(35, 35, 35)
        self.sphere_fish.setColor(1, 0, 0)
        self.sphere_fish.setTransparency(0)
        self.sphere_fish.setAlphaScale(.9)

        self.fish_uvec = self.loader.loadModel("sphere-highpoly")
        self.fish_uvec.reparentTo(self.render)
        self.fish_uvec.setScale(.01, .01, .01)
        self.fish_uvec.setColor(1, 1, 1)

        # Add the spinCameraTask procedure to the task manager.
        self.iteration = 0
        self.taskMgr.add(self.movepara, "movepara")

    # Define a procedure to move the camera.
    def exitmodel(self):
#        self.closeWindow(self.win)
#        self.taskMgr.add(sys.exit, "sys.exit")
#        self.userExit()
#        self.destroy()
        sys.exit()

#        sys.exit()
#        self.userExit()
#        self.destroy()
#        sys.exit()
        
    def movepara(self, task):
        floor_slowdown = 2
        curr_frame = np.floor(self.iteration / floor_slowdown).astype(np.int)
        print curr_frame
        if curr_frame == len(self.fish_position) - 1:
            self.iteration = 0
            curr_frame = 0
        para_positions = self.para_positions[:, curr_frame]
        fish_position = self.fish_position[curr_frame]
        fish_orientation = self.fish_orientation[curr_frame]

        for i in np.arange(0, self.numpara, 3):
            x = para_positions[i]
            y = para_positions[i+1]
            z = para_positions[i+2]
            if not np.isnan(x) and not np.isnan(y) and not np.isnan(z):
                self.spheres[i/3].show()
                self.spheres[i/3].setPos(x, y, z)
            else:
                self.spheres[i/3].hide()
        x_fish = fish_position[0]
        y_fish = fish_position[1]
        z_fish = fish_position[2]
        correction = 100
        correction_x = fish_orientation[0]*correction
        correction_y = fish_orientation[1]*correction
        correction_z = fish_orientation[2]*correction

        ux = fish_orientation[0]*500
        uy = fish_orientation[1]*500
        uz = fish_orientation[2]*500

        for i in range(int(self.numpara/3)):
            self.spheres[i].lookAt(self.sphere_fish)
        self.sphere_fish.setPos(x_fish, y_fish, z_fish)        
        if self.strikelist[curr_frame]:
            text = pandac.PandaModules.TextNode('node name')
            text.setText('STRIKE')
            textNodePath = self.sphere_fish.attachNewNode(text)
            textNodePath.setScale(3)
            textNodePath.setTwoSided(True)
            textNodePath.setPos(-15, 0, 0)
            textNodePath.setHpr(120, 0, 0)

        self.fish_uvec.setPos(x_fish - ux, y_fish - uy, z_fish - uz)
        self.fishcone.setPos(x_fish + correction_x,
                             y_fish + correction_y,
                             z_fish + correction_z)
        self.fishcone.lookAt(self.fish_uvec)
        if self.iteration == self.numframes * floor_slowdown:
            self.iteration = 0
        else:
            self.iteration += 1
        return Task.cont


app = MyApp()
app.run()


