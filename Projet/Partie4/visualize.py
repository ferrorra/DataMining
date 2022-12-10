
import importlib
import turtle
importlib.reload(turtle)
import time


def drawtree(root, X):
    def height(root):
        return 1.3 + max(height(root.left), height(root.right)) if root else -1
    def jumpto(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()
    def draw(node, x, y, dx):
        if node:
            t.goto(x, y)
            jumpto(x, y-20)
            if node.val==0: 
                cls = 'No' 
                t.pencolor('red')
            else: 
                cls='Yes'
                t.pencolor('green')
            text = "Feature : {},\n Threshold:{:.2f} ,\n Cost : {:.2f}\n ,Class:{} ,\n".format(X.columns[node.feature_index], node.threshold, node.cost, cls)
            t.write(text, align='center', font=('Arial', 5, 'normal'))
            draw(node.left, x-dx, y-60, dx/2)
            jumpto(x, y-20)
            draw(node.right, x+dx, y-60, dx/2)

    t = turtle.Turtle()


    t.speed(0); turtle.delay(0)
    h = height(root)
    jumpto(0, 30*h)
    draw(root, 0, 30*h, 40*h)
    t.hideturtle()
    turtle.done()






