import random

#The Enigma object.
#Takes six index lists as arguments, and an empty dictionary that should probably made internally.
#Has two internal functions:
    #Encoding messages.
    #Changing the rotors or plug board.
class Enigma:
    def __init__(self, rotor1_f, rotor1_b, rotor2_f, rotor2_b, rotor3_f, rotor3_b, plugs):
        self.rotor1_f = rotor1_f
        self.rotor1_b = rotor1_b
        self.rotor2_f = rotor2_f
        self.rotor2_b = rotor2_b
        self.rotor3_f = rotor3_f
        self.rotor3_b = rotor3_b
        self.plugs = plugs
        self.offset1 = 0
        self.offset2 = 0
        self.offset3 = 0
        self.master  = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    #Right, so, this is a pile of math. 
    #Long story short it uses a pair of index lists to represent each rotor, with the rotors rotation
    #being tracked via the 'offset' variables. Indexes are used instead of characters for ease of tracking.
    def encode(self):
        output = ""
        print("Enter message.")
        x = input(">")
        x = x.lower()

        for letter in x:
            #Only alphabetica characters are encoded. Spaces, numbers, punctuation, etc is ignored.
            if letter in self.master:

                in_i1 = self.master.index(letter)

                if in_i1 in self.plugs:
                    in_i1 = self.plugs[in_i1]

                in_i1 += self.offset1
                if in_i1 > 25:
                    in_i1 -= 26
                in_o1 = self.rotor1_f[in_i1]
                in_o1 -= self.offset1
                if in_o1 < 0:
                    in_o1 += 26

                in_i2 = in_o1
                in_i2 += self.offset2
                if in_i2 > 25:
                    in_i2 -= 26
                in_o2 = self.rotor2_f[in_i2]
                in_o2 -= self.offset2
                if in_o2 < 0:
                    in_o2 += 26

                in_i3 = in_o2
                in_i3 += self.offset3
                if in_i3 > 25:
                    in_i3 -= 26
                in_o3 = self.rotor3_f[in_i3]
                in_o3 -= self.offset3
                if in_o3 < 0:
                    in_o3 += 26

                out_i3 = in_o3 + 13
                if out_i3 > 25:
                    out_i3 -= 26

                out_i3 += self.offset3
                if out_i3 > 25:
                    out_i3 -= 26
                out_o3 = self.rotor3_b[out_i3]
                out_o3 -= self.offset3
                if out_o3 < 0:
                    out_o3 += 26

                out_i2 = out_o3
                out_i2 += self.offset2
                if out_i2 > 25:
                    out_i2 -= 26
                out_o2 = self.rotor2_b[out_i2]
                out_o2 -= self.offset2
                if out_o2 < 0:
                    out_o2 += 26

                out_i1 = out_o2
                out_i1 += self.offset1
                if out_i1 > 25:
                    out_i1 -= 26
                out_o1 = self.rotor1_b[out_i1]
                out_o1 -= self.offset1
                if out_o1 < 0:
                    out_o1 += 26

                #The rotors increment after each letter through the machine.
                self.offset1 += 1
                if self.offset1 > 25:
                    self.offset1 -= 26
                    self.offset2 += 1
                if self.offset2 > 25:
                    self.offset2 -= 26
                    self.offset3 += 1
                if self.offset3 > 25:
                    self.offset3 -= 26

                if out_o1 in self.plugs:
                    out_o1 = self.plugs[out_o1]

                final = self.master[out_o1]

                output += final

            else:
                output += letter
        
        print("Your encoded message: " + output)
        return

    #Allows for character mapping with the plug board, allows rotors to be swapped, 
    #and allows for manual adjustment of the rotor offset. 
    def modify(self):

        #Plug board. Uses a dictionary for easy of use.
        print("Change Plugs? (y/n)")
        if input(">") == "y":
            while True:
                self.plugs = {}
                taken = []
                print("Enter the number of plugs you want to use. (0 to 10)")
                pnum = input(">")
                pnum = int(pnum)
                if pnum > 10 or pnum < 0:
                    print("Invalid number entered.")
                else:
                    break
            for i in range(pnum):
                while True:
                    print("Enter first letter in pair. (A-Z)")
                    l1 = input(">")
                    l1 = l1.lower()
                    print("Enter second letter in pair. (A-Z)")
                    l2 = input(">")
                    l2 = l2.lower()
                    if (ord(l1) > 96 and ord(l1) < 123) and (ord(l2) > 96 and ord(l2) < 123):
                        check = False
                        if l1 in taken or l2 in taken:
                            check = True
                        if check == False:
                            taken.append(l1)
                            taken.append(l2)
                            self.plugs[self.master.index(l1)] = self.master.index(l2)
                            self.plugs[self.master.index(l2)] = self.master.index(l1)
                            break
                        else:
                            print("Invalid character entered. Character already used.")
                    else:
                        print("Invalid character entered. Must be a letter.")

        #Rotor selection. Uses the 'rotorWheels' helper function.
        print("Swap rotors? (y/n)")
        if input(">") == "y":
            self.rotor1_f, self.rotor1_b, self.rotor2_f, self.rotor2_b, self.rotor3_f, self.rotor3_b = rotorWheels()

        #Rotor offset. Takes in three numbers and sets the offset values accordingly. 
        print("Set rotor offset? (y/n)")
        if input(">") == "y":
            i = 0
            off = []
            while i < 3:
                print("Enter offset for rotor", i, "(0 to 25)")
                x = input(">")
                x = int(x)
                if x >= 0 and x <= 25:
                    off.append(x)
                    i += 1
                else:
                    print("Invalid number.")
            self.offset1 = off[0]
            self.offset2 = off[1]
            self.offset3 = off[2]

        print("Modification complete.")
        return 

#The main function makes the initial call to 'rotorWheels' and makes an engima
#object. After that it enters a loop to call the different enigma functions.
def main():
    r1f, r1b, r2f, r2b, r3f, r3b = rotorWheels()
    p = {}
    box = Enigma(r1f, r1b, r2f, r2b, r3f, r3b, p)
    while True:
        print("Enigma Machine. Enter E to Encode. Enter M to Modify. Enter Q to Quit.")
        answer1 = input(">")
        if answer1 == "E":
            box.encode()
        elif answer1 == "M":
            box.modify()
        elif answer1 == "Q":
            break
        else:
            print("Invalid Input.")


#Takes in a 'rotor wheel string' and converts it into a pair of index lists. 
#For example, B mapping to H would be 1 mapping to 7. r1_f[1] = 7, r1_b[7] = 1
def convert(r):
    master = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    r1_f = {}
    r1_b = {}
    
    i = 0
    while i < 26:
        a = r[i]
        b = master.index(a)
        r1_f[i] = b
        r1_b[b] = i
        i += 1
    
    return r1_f, r1_b


#This function calls the 'convert' helper function, passing in the 'rotor wheel strings' and 
#collecting the resultant index lists. It also let's the user choose which three rotors to use.
#Also, apparently I'm using the swiss enigma rotors. Whoops.
def rotorWheels():
    w1 = "PEZUOHXSCVFMTBGLRINQJWAYDK"
    w2 = "ZOUESYDKFWPCIQXHMVBLGNJRAT"
    w3 = "EHRVXGAOBQUSIMZFLYNWKTPDJC"
    w4 = "IMETCGFRAYSQBZXWLHKDVUPOJN"
    w5 = "QWERTZUIOASDFGHJKPYXCVBNML"

    w1 = w1.lower()
    w2 = w2.lower()
    w3 = w3.lower()
    w4 = w4.lower()
    w5 = w5.lower()

    pile = [w1, w2, w3, w4, w5]

    r_f = []
    r_b = []

    for item in pile:
        f, b = convert(item)
        r_f.append(f)
        r_b.append(b)

    #Alright so we end up with r_f and r_b each with five index lists inside. 

    taken = []
    i = 0
    while i < 3:
        print("Choose which rotor to use for position", i, "(1 to 5)")
        x = input(">")
        x = int(x)
        if x not in taken:
            if x < 6 and x > 0:
                taken.append(x)
                i += 1
            else:
                print("Invalid number.")
        else:
            print("Invalid input.")

    return r_f[taken[0]-1], r_b[taken[0]-1], r_f[taken[1]-1], r_b[taken[1]-1], r_f[taken[2]-1], r_b[taken[2]-1]

main()