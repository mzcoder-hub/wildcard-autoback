import random, time, os, sys, webbrowser, requests, hashlib, cryptocode, json

c = requests.session()

def getnew(token,refresh,key):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Privy-App-Id": "clvdnjki00bvbzqjkecroowp3",
        "Privy-Ca-Id": "c21833fc-e7a3-4851-b0da-8e9d62ad1b1d",
        "Privy-Client": "react-auth:1.67.0",
        "Referer": "https://app.wildcard.lol/",
        "Origin": "https://app.wildcard.lol",
        "Authorization": f"Bearer {token}"
    }
    final = c.post("https://auth.privy.io/api/v1/sessions",headers=head,json={"refresh_token": refresh}).json()
    data_to_encrypt = json.dumps({'token': final['token'], 'refresh': final['refresh_token'],'key': key})
    dones = cryptocode.encrypt(data_to_encrypt, key)
    with open('token.txt', 'w') as f:
        f.write(dones)
        f.close()
    return

def log():
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Privy-App-Id": "clvdnjki00bvbzqjkecroowp3",
        "Privy-Ca-Id": "c21833fc-e7a3-4851-b0da-8e9d62ad1b1d",
        "Privy-Client": "react-auth:1.67.0",
        "Referer": "https://app.wildcard.lol/",
        "Origin": "https://app.wildcard.lol"
    }
    login = c.post("https://auth.privy.io/api/v1/farcaster/init",headers=head,json={}).json()
    urlny = login["connect_uri"]
    head["Farcaster-Channel-Token"] = login["channel_token"]
    webbrowser.open(urlny)
    return head,login["channel_token"]

def check(head):
    datax =  c.get("https://auth.privy.io/api/v1/farcaster/status",headers=head[0]).json()
    if(datax["state"] == "pending"):
        sys.stdout.write(f'\rLoading User Login |')
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write(f'\rLoading User Login /')
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write(f'\rLoading User Login -')
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write(f'\rLoading User Login \\')
        sys.stdout.flush()
        check(head)
    else:
        datanya = {
            "channel_token": head[1],
            "fid": datax["fid"],
            "message": datax["message"],
            "signature": datax["signature"]
        }
        done = c.post("https://auth.privy.io/api/v1/farcaster/authenticate",headers=head[0],json=datanya).json()
        encryption_key = hashlib.sha256(str("PandaEver").encode('utf-8')).hexdigest()
        data_to_encrypt = json.dumps({'token': done['token'], 'refresh': done['refresh_token'], 'key': encryption_key})
        dones = cryptocode.encrypt(data_to_encrypt, encryption_key)
        with open('token.txt', 'w') as f:
            f.write(dones)
        f.close()
        print("\nLogin Success")

def remaining(token):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://app.wildcard.lol/",
        "Origin": "https://app.wildcard.lol",
        "Authorization": f"Bearer {token}"
    }
    mydat = c.get("https://sys.wildcard.lol/app/my_profile",headers=head).json()
    return int(mydat["tipping_allowance"]["value"]), mydat["farcaster_user"]["username"]

def getlasttip(token):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://app.wildcard.lol/",
        "Origin": "https://app.wildcard.lol",
        "Authorization": f"Bearer {token}"
    }
    last = c.get("https://sys.wildcard.lol/app/my_transactions/tips",headers=head).json()
    if(last == []):
        roken = remaining(token)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' |')
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' /')
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' -')
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' \\')
        sys.stdout.flush()
        time.sleep(0.2)
    elif(last[0]["tip_given"] == False):
        if(remaining(token)[0] >= int(last[0]["tip_amount"]["amount"])):
            another = c.get("https://sys.wildcard.lol/app/casts/"+last[0]["from_user"]["username"],headers=head).json()
            tot = -1
            for item in another:
                tot = tot+1
            randomizedcast = random.randint(0, tot)
            tip(head, another[randomizedcast]["cast"]["id"], last[0]["from_user"]["fid"], last[0]["tip_amount"]["amount"], last[0]["from_user"]["username"])
        elif(remaining(token)[0] != 0):
            another = c.get("https://sys.wildcard.lol/app/casts/"+last[0]["from_user"]["username"],headers=head).json()
            tot = -1
            for item in another:
                tot = tot+1
            randomizedcast = random.randint(0, tot)
            tip(head, another[randomizedcast]["cast"]["id"], last[0]["from_user"]["fid"], remaining(token)[0], last[0]["from_user"]["username"])
        else:
            print("allowance is insufficient")
    else:
        roken = remaining(token)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' |')
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' /')
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' -')
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f'\rRemaining Allowance: '+ str(roken[0]) +' Username >>> '+roken[1]+' \\')
        sys.stdout.flush()
        time.sleep(0.2)


def tip(head, castid, userid, amount, username):
    finaldat = {
        "amount": int(amount),
        "currency": "WILD"
    }
    if os.path.exists("./already_tipped.txt"):
        with open('already_tipped.txt', 'r') as userny:
            data_username = userny.read()
    else:
        with open('already_tipped.txt', 'w') as userny:
            userny.write('[]')
            userny.close()
        with open('already_tipped.txt', 'r') as usernys:
            data_username = usernys.read()
    if username not in data_username:
        with open('already_tipped.txt', 'a') as filesny:
             filesny.write(username)
             filesny.close()
        if(c.post("https://sys.wildcard.lol/app/tip/cast/"+castid+"/"+str(userid), headers=head,json=finaldat).json()["tip"] == "success"):
            print("Success Tip: "+username)
        else:
            print("Failed Tip "+username)
    else:
        print("already tip "+username)
    

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("By: PandaEver\nGithub: JustPandaEver\nThanks To: mzcoder-hub")
    while True:
        if os.path.exists("./token.txt"):
            with open('token.txt', 'r') as f:
                tokens = f.read()
                key = hashlib.sha256(str("PandaEver").encode('utf-8')).hexdigest()
                decoded = cryptocode.decrypt(tokens, key)
                cfg = json.loads(decoded)
                getnew(cfg['token'], cfg['refresh'], key)
                with open('token.txt', 'r') as fs:
                    tokenss = fs.read()
                decodeds = cryptocode.decrypt(tokenss, key)
                cfgs = json.loads(decodeds)
                getlasttip(cfgs['token'])
        else:
            check(log())
main()
