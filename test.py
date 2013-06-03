from apu import aputime

def main():
    apu = aputime.APU('UC2F1208IT{ISS}', '2013-06-03') 
    #change the intake to see how the script works
    print apu.to_html()

if __name__ == '__main__':
    main()
