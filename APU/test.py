import aputime 

def main():
    apu = aputime.APU('UC2F1201IT{ISS}', '2012-10-08')
    print apu().to_ics()

if __name__ == '__main__':
    main()
