import sys
from pandac.PandaModules import WindowProperties
import pandac.PandaModules
# from panda3d.core import Shader
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter

pandac.PandaModules.loadPrcFileData("", """
            fullscreen 0
            load-display pandagl
            win-origin 0 0
            undecorated 0
            win-size 640 400
            sync-video 1
            """)

#  win-size 2560 1600

class MyApp(ShowBase):
    def __init__(self):
        homedir = '/Users/nightcrawler2/PreycapMaster/'
        sim_text = raw_input('Simulation Type: ')
        if sim_text[0] == 's':
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
            print para_cont_window
            para_positions = np.load(
                homedir + '3D_paracoords.npy')[:, para_cont_window:]
            fish_position = np.load(homedir + 'ufish_origin.npy')
            fish_orientation = np.load(homedir + 'ufish.npy')
            self.strikelist = np.zeros(fish_position.shape[0])

        else:
            para_positions = np.load(
                homedir + 'para_simulation' + sim_text[1] + '.npy')
            print("Para Positions")
            print(para_positions.shape[1])
            fish_position = np.load(
                homedir + 'origin_model' + sim_text[1] + '.npy')
            print("Fish_Position")
            print(fish_position.shape[0])
            fish_orientation = np.load(
                homedir + 'uf_model' + sim_text[1] + '.npy')
            print("Fish_Orientation")
            print(fish_orientation.shape[0])
            try:
                self.strikelist = np.load(homedir + 'strikelist' + sim_text[1]+ '.npy')
            except IOError:
                self.strikelist = np.zeros(fish_position.shape[0])
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

        ShowBase.__init__(self)
        self.accept("escape", self.exitmodel)
#        props = WindowProperties()
#        props.setCursorHidden(False)
#        props.setMouseMode(WindowProperties.M_absolute)
#        self.win.requestProperties(props)
        self.lens1 = pandac.PandaModules.PerspectiveLens()
#        self.lens1.setFov(120, 120)
        self.lens1.setFov(90, 90)
        self.lens1.setNearFar(0.1, 10000)
        self.lens1.setAspectRatio(1280/800.)
        self.cam.node().setLens(self.lens1)
        self.cam.setPos(0, 0, 0)
        self.setBackgroundColor(0, 0, 0, 1)
#        self.setBackgroundColor(.3, .6, .9)
        # Original Tank Boundary Lines
        # self.d2 = pandac.PandaModules.LineSegs()
        # self.d2.setColor(1, 1, 1, 1)
        # self.d2.setThickness(150)
        # self.d2.moveTo(0, 0, 0)
        # self.d2.drawTo(1888, 0, 0)
        # self.d2.moveTo(0, 0, 0)
        # self.d2.drawTo(0, 0, 1888)
        # self.d2.moveTo(0, 0, 0)
        # self.d2.drawTo(0, 1888, 0)
        self.d2 = pandac.PandaModules.LineSegs()
        self.d2.setColor(1, 1, 1, .5)
        self.d2.setThickness(1)
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


        self.fish_vect = pandac.PandaModules.LineSegs()
        self.fish_vect.setColor(0, 0, 1, 1)
        self.fish_vect.setThickness(150)
        self.fish_vect.moveTo(0, 0, 0)
        self.fish_vect.drawTo(10, 0, 0)
        geom_fish_vect = self.fish_vect.create()
        self.node_fish_vect = self.render.attachNewNode(geom_fish_vect)
        geom2 = self.d2.create()
        self.nodegeom2 = self.render.attachNewNode(geom2)

        # Load the environment model.
        self.spheres = dict({})

        for i in range(int(self.numpara/3)):
            self.spheres[i] = self.loader.loadModel("sphere")
            self.spheres[i].reparentTo(self.render)
#            self.spheres[i].setScale(5, 5, 5)
            self.spheres[i].setColor(.75, .75, .75)
            self.spheres[i].setScale(4, 4, 4)
            if sim_text == 't':
                text = pandac.PandaModules.TextNode('node name')
                text.setText(' ' + str(i))
                textNodePath = self.spheres[i].attachNewNode(text)
                textNodePath.setScale(5)
                textNodePath.setTwoSided(True)
                textNodePath.setPos(-10, 0, 0)
                textNodePath.setHpr(180, 0, 0)

        self.sphere_fish = self.loader.loadModel("sphere")
        self.sphere_fish.reparentTo(self.render)
        self.sphere_fish.setScale(5, 5, 5)
        self.sphere_fish.setColor(1, 0, 1)

        self.sphere_fish2 = self.loader.loadModel("sphere")
        self.sphere_fish2.reparentTo(self.render)
#        self.sphere_fish2.setScale(0.02, 0.02, 0.02)
        self.sphere_fish2.setScale(0.015, 0.015, 0.015)
        self.sphere_fish2.setColor(0.5, 0.1, 0.6)

        self.iteration = 0
        self.complete = False
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.movepara, "movepara")

    # Define a procedure to move the camera.
    def exitmodel(self):
        print len(self.para_positions)
        print len(self.fish_position)
        print len(self.fish_orientation)
        self.destroy()
        sys.exit()
    
    def movepara(self, task):
        floor_slowdown = 4
        curr_frame = np.floor(self.iteration / floor_slowdown).astype(np.int)
        if curr_frame >= len(self.fish_position):
            curr_frame = len(self.fish_position) - 1
        if self.complete:
            curr_frame = len(self.fish_position) - 1

        para_positions = self.para_positions[:, curr_frame]
        fish_position = self.fish_position[curr_frame]
        fish_orientation = self.fish_orientation[curr_frame]
            
        if curr_frame % 20 == 0:
            print curr_frame            
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

        dx = fish_orientation[0]*1
        dy = fish_orientation[1]*1
        dz = fish_orientation[2]*1

        for i in range(int(self.numpara/3)):
            self.spheres[i].lookAt(self.sphere_fish2)

        self.sphere_fish.setPos(x_fish, y_fish, z_fish)
        self.sphere_fish2.setPos(x_fish+dx, y_fish+dy, z_fish+dz)
        if self.strikelist[curr_frame] and not self.complete:
            print('STRIKE!!!!')
            text = pandac.PandaModules.TextNode('node name')
            text.setText('STRIKE!!')
            textNodePath = self.render.attachNewNode(text)
            textNodePath.lookAt(self.sphere_fish2)
            textNodePath.setScale(.1)
            textNodePath.setTwoSided(True)
            textNodePath.setPos(x_fish + dx + .1, y_fish + dy, z_fish + dz)
            textNodePath.setHpr(45, 0, 0)
            textNodePath.setColor(255,0,0)
            # comment out complete = True to have this run forever
            self.complete = True
        self.cam.setPos(x_fish, y_fish, z_fish)
        self.cam.lookAt(self.sphere_fish2)
        # this does same thing as base
        # self.screenshot(defaultFilename=0, namePrefix= "%05d.png" % (task.frame))

        if self.iteration == self.numframes * floor_slowdown:
#            self.iteration = 0
            pass
        else:
            self.iteration += 1

        return Task.cont
        

app = MyApp()
app.run()
