from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import math


class CarModel:
    def __init__(self, m1=1, m2=1, c1=6, k1=1, k2=4, ymag=6, v=120, ramp_angle=45, t=3):
        self.t = np.linspace(0, t, 200)
        self.ic = [0,0,0,0]
       
        #define the model parameters
        self.m1 = m1  # the car body mass
        self.m2 = m2  # tire mas
        self.c1 = c1  # damping (shock absorber)
        self.k1 = k1  # suspension spring constant
        self.k2 = k2  # tire spring constant
        self.ymag = ymag  # the magnitude of the forcing function
        self.v = v  # car speed
        self.ramp_angle = ramp_angle


    def ode_system(self, X, t, carparams, roadparams):
        # define any numerical parameters (constants)
        # these params were stored in two lists, and must be passed in the correct order!
        m1 = carparams[0]; m2=carparams[1]; c1=carparams[2]; k1=carparams[3]; k2=carparams[4]
        
        ymag = roadparams[0]

        t_ramp = (ymag/math.sin(self.ramp_angle))/self.v
        
        #define the forcing function equation
        if t < t_ramp:
            y = ymag*(t/t_ramp)
        else:
            y = ymag
        
        x1 = X[0]; x1dot=X[1]; x2=X[2]; x2dot=X[3] # copy from the state array to nicer names
        
        #write the non-trivial equations
        x1ddot = (1/m1) * (c1*(x2dot - x1dot) + k1*(x2 - x1))
        x2ddot = (1/m2) * (-c1*(x2dot - x1dot)- k1*(x2 - x1) + k2*(y - x2))
        
        #return the derivitaves of the input state vector
        return [x1dot,x1ddot,x2dot,x2ddot]

    def plot(self, ax):
        carparams = [self.m1, self.m2, self.c1, self.k1, self.k2]  #put the car parameters into a list
        roadparams = [self.ymag] #put the road parameters into a list
        
        # add axis labels
        ax.set_ylabel('Position and Velocity', fontsize='medium')
        ax.set_xlabel('Time (s)', fontsize='medium')
        
        # put a title on the plot
        ax.set_title('Car Body Dynamics', fontsize='medium')
        x = odeint(self.ode_system, self.ic, self.t,args=(carparams,roadparams))

        ax.plot(self.t, x[:,0], 'b-', label = 'Body Position')
        ax.plot(self.t, x[:,1], 'r-', label = 'Body Velocity')
        ax.axvline(x = 0, color='c')
        ax.axhline(y = 6, color='c')
        # plt.plot(self.t, x[:,0], 'b-', label = 'Body Position')
        # plt.plot(self.t, x[:,1], 'r-', label = 'Body Velocity')
        # plt.legend(loc = 'lower right')
        # plt.xlabel('Time, s')
        # plt.ylabel('Position and Velocity')
        # plt.title('Car Body Dynamics')
        # plt.show()

        ax.plot(self.t, x[:,2], 'b-', label = 'Wheel Position')
        ax.plot(self.t, x[:,3], 'r-', label = 'Wheel Velocity')

         # modify the tick marks
        ax.tick_params(axis='both', which='both', direction='in', top=True, right=True,
                       labelsize='medium')  # format tick marks
        ax.legend(loc='upper right')
        # plt.plot(self.t, x[:,2], 'b-', label = 'Wheel Position')
        # plt.plot(self.t, x[:,3], 'r-', label = 'Wheel Velocity')
        # plt.legend(loc = 'lower right')
        # plt.xlabel('Time, s')
        # plt.ylabel('Position and Velocity')
        # plt.title('Car Tire Dynamics')
        # plt.show()


def main():
    car_model = CarModel()
    car_model.plot()


if __name__ == "__main__":
    main()