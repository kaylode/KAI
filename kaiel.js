const token = process.env.TOKENJS;
const { Client, Message } = require('discord.js');
const { DiscordSR } = require('discord-speech-recognition');

const client = new Client();
const discordSR = new DiscordSR(client);

client.once('ready', () => {
    console.log('Ready!');
});

var channel = null;

client.on('message', message => {
    if (message.author.id != client.user.id) {
        if (message.content=='$listen on') {
            message.member.voice.channel.join();
            channel = message.channel;
        }

        if (message.content=='$listen off') {
            message.member.voice.channel.leave();
        }
    }
})

client.on('speech', message => {

    let response = message.content;
    var tokens;
    try{
        tokens = response.split(" ");
        let trigger = tokens[0];
        switch(trigger) {
            case "play":
            case "skip":
            case "pause":
            case "resume":
            case "wiki":
            case "voice":
            case "listen":
              response = "$".concat(response);
              channel.send(response);
              console.log(response);     
              break;
          default:
              console.log(response);     
        }
    }
    catch (err) {
        console.log('Undefined')
    }
})

client.login(token);
