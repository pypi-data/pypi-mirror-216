# **How to use the ARIclicker?**

## **explanation:** 

"ARIclicker" is "Auto Random Interval clicker".

 This is a very good autoclicker, easy to use and intelligent.


## **First of all** 

You need to install **ARIclicker**: Open `cmd` and type `pip install ARIclicker`


# **syntax:**

## **clicker**:

(autoclick)
`
ARIclicker.autoclick(start_stop_key_character, end_key_character, button,delay_min=None, delay_max=None, delay=None)
`

(quickclick)
`
ARIclicker.quickclick(key_start,key_stop,program_stop_key=None,delay_min=None,delay_max=None,delay=None)
`

## **presser**:
`
ARIclicker.autopress("start_pause_key","end_key","pressed_button")
`

example 1:
<pre>
	import ARIclicker 
	ARIclicker.autoclick("a","b","left",delay_min=0.1,delay_max=1)
</pre>

**explanation:** If you press the "a" key, clicking will start. When you press the "a" key again, clicking will pause. When you press the "b" key, the program will exit. The range of click intervals is between 0.1 and 1 second, and the left mouse button is the key clicked.

example 2:
<pre>
	import ARIclicker
	ARIclicker.autopress("a","b","c")
</pre>


**explanation:** If you press the "a" key,pressing will start.When you press the "a" key again, pressing will pause.When you press the "b" key, the program will exit.The 'c' key represents the key that will be pressed.

example 3:
<pre>
	import ARIclicker
	ARIclicker.quickclick("a","b",delay_min=0.1,delay_max=1)
</pre>


 ## **have fun~**










