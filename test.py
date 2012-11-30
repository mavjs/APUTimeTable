from APU import aputime

def main():
    apu = aputime.apu('UC2F1208IT{ISS}', '2012-11-26') 
    #change the intake to see how the script works
    print apu.to_ics()
    print apu.to_html()

if __name__ == '__main__':
    main()
