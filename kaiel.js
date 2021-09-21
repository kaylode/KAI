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
    if (message.author.id != client.user.id && message.content=='$listen') {
        message.member.voice.channel.join();
        channel = message.channel;
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
              response = "$".concat(response);
              channel.send(response);
              break;
          default:
              console.log(response);     
        }
    }
    catch (err) {
        console.log(err.message)
    }
})

client.login(token);
