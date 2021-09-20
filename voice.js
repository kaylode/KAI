const token = process.env.TOKEN;

const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.once('ready', () => {
    console.log('Ready!');
});

client.on('message', async message => {
    if (message.author.id != client.user.id && message.content=='$join') {
        const connection = await message.member.voice.channel.join();
        
        const receiver = connection.receiver.createStream(message.member, {
          mode: "pcm",
          end: "silence"
        });

        const writer = receiver.pipe(fs.createWriteStream('./.cache/recording.pcm'));
        
        writer.on('finish', () => {
            console.log('Finish recording')
        });
    }
});

client.login(token);
