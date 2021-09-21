const token = process.env.TOKENJS;

const fs = require('fs');
const Discord = require('discord.js');
const client = new Discord.Client();

client.once('ready', () => {
    console.log('Ready!');
});

client.on('message', async message => {
    if (message.author.id != client.user.id && message.content=='$listen') {
        const connection = await message.member.voice.channel.join();

        // DiscordJS listens twice, the second time is empty audio so use trick
        var i = 0;
        connection.on('speaking', (user, speaking) => {
            if (speaking && ((i % 2)==0) && user.username=='Kaylode') {
                i += 1;
                console.log(`I'm listening to ${user.username}`);

                const receiver = connection.receiver.createStream(message.member, {
                    mode: "pcm",
                    end: "silence"
                });

                const writer = receiver.pipe(fs.createWriteStream('./.cache/recording.pcm'));
                  
                writer.on('finish', () => {
                    console.log('Finish recording')
                });

            } else {
              i = 0;
            }
            
        });
        
        
    }
});

client.login(token);
