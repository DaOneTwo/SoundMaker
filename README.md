# SoundMaker

Sound Maker is a simple application which contains both client and
server code that will enable remote systems to cause noise to be made on
the server system via a network connection.

The goal in of the application is to get brand new students excited
about the possibilities presented by programming. I hope to accomplish
this by allowing them to get a remote system to respond audibly to the
commands they program. Within minutes of getting python 3 installed on
their system.

The code is in no way intended to be any sort of production ready code.
It was built for and intended to be run in a "controlled" classroom type
environment.

### Text To Speech


There is text-to-speech code that has the server system "vocalize" the
text contained within the client code. The client programmer can specify
both the voice to be used and the text to be vocalized.

Voices available may be dependent upon the system on which the server is
running.


This list is from my OSX (Mac) system. Your list may be a little
different.

'Alex', 'Alice', 'Alva', 'Amelie', 'Anna', 'Carmit', 'Damayanti', 'Daniel', 'Diego', 'Ellen', 'Fiona', 'Fred', 'Ioana', 'Joana', 'Jorge', 'Juan', 'Kanya', 'Karen', 'Kyoko', 'Laura', 'Lekha', 'Luca', 'Luciana', 'Maged', 'Mariska', 'Mei-Jia', 'Melina', 'Milena', 'Moira', 'Monica', 'Nora', 'Paulina', 'Samantha', 'Sara', 'Satu', 'Sin-ji', 'Tessa', 'Thomas', 'Ting-Ting', 'Veena', 'Victoria', 'Xander', 'Yelda', 'Yuna', 'Yuri', 'Zosia', 'Zuzana'

### client.py

The client.py file contains a program built to communicate with a remote
computer that is running the server (server.py). The remote computer can
actually be your computer too that will be addressed later in these in
these instructions.

To get things working properly you will need to open the file in some
sort of text editor. At the bottom of the file you will find some text
that looks like this...

```python
if __name__ == '__main__':
    sc = TextToSpeechClient(name='Your Name Here', server_ip='127.0.0.1')

    # sc.say('Samantha', 'Knock Knock')
```

You will need to make a few changes and then save the file. The
changes needed are...

1. put your name in the parenthesis following the name=
2. put the destination server's ip in the appropriate place in a similar
manner. 127.0.0.1 is your local machine so if you are running both the
server and the client you do not have to change the server ip.

Once those changes are saved go ahead and run the file and see what
happens.

Open a command prompt (terminal) and type the command

`python3 /path/to/your/file/client.py`

Once you have ran the file the first time there are some additional
lines below the one you just changed. Experiment with removing the "#"
comment characters on those lines. Then save and run the file again to
see what happens. Once you have done that you can experiment as you like
just remember to keep things "clean".

### server.py

The server.py file contains code which listens for requests made from
clients. If the request contains information in a format which it can
process then it will do as asked. Otherwise it will just ignore it.

The server has a few functionalities beyond the core python
capabilities. That means there is a little additional setup needed to be
able to run the file. We need to install a few files.

While not a requirement, I recommend using a python virtual environment.
Cross platform (OS System) instructions directly from the python
software foundation can be
[found here.](https://docs.python.org/3/library/venv.html)

From a command prompt make sure you are in the main SoundMaker
directory. If you are using a virtual environment make sure it is
activated.

```bash
pip install -r requirements.txt
```

this command will install the modules (other peoples code) that we
depend on to be able to convert the text to speech and play sounds.

After this completes you should be ready to run the server. In the same
terminal you run the server.py file.

```bash
python3 server.py
```

you should see some things print to the terminal one of the lines should
say the server is ready. If so you are ready to go start sending
commands to your server with the client.py file. Remember your IP will
be 127.0.0.1 or localhost will work too.


### Running client.py file

The client.py file contains a program built to communicate with a remote
computer that is running the server.

To get things working properly you will need to open the file in some
sort of text editor. At the bottom of the file you will find some text
that looks like this...

```python
if __name__ == '__main__':
    sc = TextToSpeechClient(name='Your Name Here', server_ip='127.0.0.1')

    # sc.say('Samantha', 'Knock Knock')
```

You will need to make a few changes and then save it. The changes needed
are...

* put your name in the parenthesis following the name=
* put the destination server's ip in the appropriate place in a similar
  manner

Once those changes are saved go ahead and run the file and see what
happens.

Open a command prompt (terminal) and type the command

`python3 /path/to/your/file/client.py`

Once you have ran the file the first time there are some additional
lines below the one you just changed. Experiment with removing the #
characters on those lines. Then save and run the file again to see what
happens. Once you have done that you can experiment as you like just
remember to keep things "clean".
