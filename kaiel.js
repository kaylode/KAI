const token = process.env.TOKENJS;
const { Client, Message } = require('discord.js');
const { DiscordSR,  DiscordSROptions, resolveSpeechWithGoogleSpeechV2 } = require('discord-speech-recognition');

const client = new Client();
const discordSR = new DiscordSR(client, {
  lang: "vi-VN",
  speechRecognition: resolveSpeechWithGoogleSpeechV2,
});

const db = require('./database/db.json');
var dict = db['voice'];

function mapTriggerWords(text){
    let result = text;
    let tokens = text.split(" ");
    let triggers = [tokens[0], tokens.slice(0,2).join(' ')];
    for (const tr of triggers) {
        if (tr in dict) {
            console.log(tr);
            result = dict[tr][0];
            result = result.concat(' ', tokens.slice(2).join(' '));
            return result;
        }
    }
    return result;
}

client.once('ready', () => {
    console.log('Ready!');
});

var channel = null;

client.on('message', message => {
    if (message.author.id != client.user.id) {
        if (message.content=='$listen on') {
            message.member.voice.channel.join();
            channel = message.channel;
            channel.send("Vui lòng nói lớn, tao mới nghe được.");
        }
    }

    if (message.content=='$listen off') {
        message.member.voice.channel.leave();
        channel.send("Tạm biệt.");
    }
})

client.on('speech', message => {

    let response = message.content;
    var tokens;
    try{
        response = response.toLowerCase();
        response = mapTriggerWords(response);
        tokens = response.split(" ");
        let trigger = tokens[0];
        switch(trigger) {
            case "play":
            case "skip":
            case "continue":
            case "next":
            case "pause":
            case "stop":
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