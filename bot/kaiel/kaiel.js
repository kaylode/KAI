const keep_alive = require('./server.js')
const token = process.env.TOKENJS;
const { Client, Message } = require('discord.js');
const { DiscordSR,  DiscordSROptions, resolveSpeechWithGoogleSpeechV2, VoiceMessage } = require('discord-speech-recognition');

var client = new Client();
var discordSR = new DiscordSR(client, {
  lang: "vi-VN",
  speechRecognition: resolveSpeechWithGoogleSpeechV2,
});

// Console log counter
var console_logs = [];
var previos_message = null;
// Load mapping from database
const db = require('./database/db.json');
var dict = db['voice'];
var word_triggers = db['words'];

function mapTriggerWords(text){
    // Map trigger voice words into trigger commands
    
    let result = text;
    let tokens = text.split(" ");

    let length = tokens.length;
    for (let i = 0; i < length; i++) {
        let trigger_tokens = tokens.slice(0,i+1)
        let trigger = trigger_tokens.join(' ');
        if (trigger in dict) {
            result = dict[trigger][0];
            result = result.concat(' ', tokens.slice(trigger_tokens.length).join(' '));
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
            previos_message = message;
            channel.send("Vui lòng nói lớn, tao mới nghe được.");
        }
    }

    if (message.content=='$listen off') {
        message.member.voice.channel.leave();
        previos_message = message;
        channel.send("Tạm biệt.");
    }

    if (message.content=='$listen vietnam' || message.content=='$listen việt nam') {
        console.log('Chuyển sang Tiếng Việt');
        discordSR.speechOptions = {
            lang: "vi-VN",
            speechRecognition: resolveSpeechWithGoogleSpeechV2,
        };
    }

    if (message.content=='$listen english') {
        discordSR.speechOptions = {
            lang: "en-US",
            speechRecognition: resolveSpeechWithGoogleSpeechV2,
        };
        console.log('Change to English');
    }
})

client.on('speech', message => {
    // If speech detected, do
    let user = message.author.username;
    let isbot = message.author.isbot;
    let duration = message.duration;
    let response = message.content;

    console_logs.push(response)
    if (console_logs.length >= 50){
        console.clear();
        console_logs = [];
    }

    if ((parseFloat(duration) > 10) || (typeof(response) == "undefined") || isbot) {
        console.log(user.concat(': ', String(response), ' (', duration, ')')); 
    } else {
        var tokens;
        response = response.toLowerCase();
        response = mapTriggerWords(response);

        // Detect bad words
        Object.entries(word_triggers).forEach(([key, values]) => {
            if (response.includes(key)){
                value = values[Math.floor(Math.random() *values.length)]
                if (value.includes('{name}')){
                    value = value.replace('{name}', user);
                }
                channel.send(value);
            }      
         });

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
            case "remove":
            case "wiki":
            case "voice":
            case "listen":
            case "clear":
            case "queue":
            case "shuffle":   
              response = "$".concat(response);
              channel.send(response);
              break;
          default:
              break;
        }
        console.log(user.concat(': ', response, ' (', duration, ')'));             
    }
})

client.login(token);