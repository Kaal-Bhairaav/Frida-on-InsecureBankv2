import frida, sys

def on_message(message, data):
	if message['type'] == 'send':
		print("[*] {0}".format(message['payload']))
	else:
		print(message)

code = """
Java.perform(function () {
	var main = Java.use('com.android.insecurebankv2.PostLogin');
	var bool = Java.use('java.lang.Boolean');

	main.checkIfDeviceIsEmulator.implementation = function () {
	send("Return False in checkIfDeviceIsEmulator");
	var boolvar = bool.$new("false");
	return boolvar;
	};

	main.doesSuperuserApkExist.implementation = function () {
	send("Return False in doesSuperuserApkExist");
	return false;
	};

	main.doesSUexist.implementation = function () {
        send("Return False in doesSUexist");
        return false;
        };


});
"""

process = frida.get_usb_device().attach('com.android.insecurebankv2')
script = process.create_script(code)
script.on('message', on_message)
script.load()
sys.stdin.read()
