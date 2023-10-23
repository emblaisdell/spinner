from math import sqrt
import time
import vtkmodules.all as vtk

phi = (1 + sqrt(5)) * 0.5
dR = 2 - phi


class vtkTimerCallback:
    def __init__(
        self, steps: int, actor: vtk.vtkActor, interactor: vtk.vtkRenderWindowInteractor
    ):
        self.timer_count = 0
        self.steps = steps
        self.actor = actor
        self.interactor = interactor
        self.timerID = None

    def execute(self, obj: vtk.vtkRenderWindowInteractor, event):
        step = 0

        while True:
            print(self.timer_count)
            self.actor.SetOrientation(0, -360 * dR * self.timer_count, 0)
            interactor = obj
            interactor.GetRenderWindow().Render()
            self.timer_count += 1
            step += 1
            time.sleep(0.03)

        if self.timerID:
            interactor.DestroyTimer(self.timerID)


def main():
    reader = vtk.vtkSTLReader()
    reader.SetFileName("./main.stl")

    # Create mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.GetProperty().SetColor(0.5, 0.5, 0.5)
    actor.SetMapper(mapper)
    # actor.SetPosition(0, 0, 0)

    # setup renderer and interactor
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.1, 0.1)
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("Animation test")
    render_window.SetSize(600, 600)
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Add actor to the scene
    renderer.AddActor(actor)

    # Render and interact
    render_window.Render()
    camera = renderer.GetActiveCamera()
    camera.Zoom(1.5)
    # print(camera.GetPosition())
    camera.SetClippingRange(1, 20)
    camera.SetPosition(0, 5, 10)
    render_window.Render()

    # initialize - prior to creating timer event
    interactor.Initialize()

    # sign up to timer event
    cb = vtkTimerCallback(50000, actor, interactor)
    interactor.AddObserver("TimerEvent", cb.execute)

    cb.timerID = interactor.CreateRepeatingTimer(3000)

    # start the interaction and timer
    render_window.Render()
    interactor.Start()


if __name__ == "__main__":
    main()
