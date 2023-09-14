class sampler():
    def __init__(self, size, sensor_max):
        
        if (size%2) == 0: self.size = size + 1                        # If size is even, add 1 to make it un-even so sample range 
        else: self.size = size                                        # can have a single middle value, else if uneven, accept
        self.middle_index = int((self.size - 1) / 2)                  # Calculate middle index
        self.samples = [0]*self.size                                  # Create list to hold sampled values
        self.sensor_max = sensor_max                                  # sensor_max is used to ignore rogue readings
        self.index = 0                                                # Set index to zero
    
    
    def set_baseline(self, reading):                                  # When setting a baseline readings should not be 
                                                                      # tested against self.get_averaged_median()
        if reading < self.sensor_max:                                 # Reading should only be tested against sensor_max
            self.samples[self.index] = reading                        # If the reading is valid, store it
            self.index += 1                                           # This function should be called in a for loop:
            if self.index == self.size: self.index = 0                # for index, val in enumerate(sampler.samples):  sampler.set_baseline(read_sensor())
        
        
    def store(self, new_reading):                                     # When storing a single reading it should not be
                                                                      # 'too far off' self.get_averaged_median(xx)
        if abs(self.get_averaged_median(40) - new_reading) < 100:     # This way the reference (averaged mean) can change slightly in time
            self.samples[self.index] = new_reading                    # to account for sensor drift. While at the same time
            self.index += 1                                           # alert readings do not influence the averaged mean
            if self.index == self.size: self.index = 0
     
    # Get single middle value
    def get_median(self):                                                 
        
        self.samples.sort()                                           # Sort the list of samples
        return self.samples[self.middle_index]                        # Return the middle value
    
    # Get average of a middle subset
    def get_averaged_median(self, percent):                                       
        
        offset = round(self.size * (percent/2) / 100)                                       # Calculate start/end offset from middle
        subset = self.samples[self.middle_index - offset : self.middle_index + offset]      # Create subset
        return round(sum(subset)/len(subset)) 

if __name__ == '__main__':
    print('tank math demo')
    vals = [1, 5, 10, 11,11,12,1,1,1,1,1,4,6,3,7,4]
    s = sampler(3, 200)
    for i in vals:
        s.store(i)
    print(f'median:  {s.get_median()}')
    print(f'average: {s.get_averaged_median(75)}')
