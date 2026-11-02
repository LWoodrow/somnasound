import { WebClient } from '@slack/web-api';

const token = process.env.SLACK_BOT_TOKEN;
const client = new WebClient(token);

async function run() {
  try {
    await client.chat.postMessage({
      channel: 'C0CDFJV5BHV',
      text: '? *Somnasound Multi-Agent Operational Command Online.* Harness initialization successful.',
    });
    console.log('Handshake successful! Check your Slack channel.');
  } catch (error) {
    console.error('Connection failed:', error);
  }
}

run();
