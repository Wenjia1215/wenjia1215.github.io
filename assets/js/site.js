(() => {
  'use strict';

  const terminalLog = document.querySelector('#terminalLog');
  const terminalForm = document.querySelector('#terminalForm');
  const terminalInput = document.querySelector('#terminalInput');
  const asciiFace = document.querySelector('#asciiFace');
  const canvas = document.querySelector('#portraitCanvas');
  const numberRain = document.querySelector('#numberRain');

  const links = {
    github: 'https://github.com/Wenjia1215',
    linkedin: 'https://www.linkedin.com/in/wenjiawang-page/',
    scholar: 'https://scholar.google.com/citations?user=Zl-yM-kAAAAJ&hl=en&oi=ao',
    youtube: 'https://www.youtube.com/@WenjiaCybersecurity',
    cv: 'assets/files/wenjia-wang-cv.pdf',
    email: 'mailto:wenjiabusiness@gmail.com',
  };

  const bootSequence = [
    {
      command: 'whoami',
      output: [
        'wenjia wang · cs ph.d. candidate · trustworthy ai / cybersecurity / cs education',
      ],
    },
    {
      command: 'cat about.txt',
      output: [
        'building verifiable ai for compliance, retrieval, and high-stakes qa.',
        'teaching cs through systems students build, test, debug, and explain.',
      ],
    },
    {
      command: 'ls skills/',
      output: [
        '<a href="publications.html">verifiable-ai</a> · citation grounding · retrieval · runtime checks',
        '<a href="publications.html">cybersecurity</a> · compliance · zero trust · cloud security',
        '<a href="teaching.html">teaching</a> · programming · ai apps · software engineering · capstone',
      ],
    },
    {
      command: 'ls work/',
      output: [
        'ComplianceGPT <span class="flag">[research]</span> · evidence-grounded compliance qa',
        'Zero Trust migration <span class="flag">[paper]</span> · overlays for legacy infrastructure',
        'Baby-Feed <span class="flag">[health]</span> · healthcare web app + pilot trial',
        'FIU Capstone <span class="flag">[service]</span> · mentor + showcase judge since fall 2021',
      ],
    },
    {
      command: 'echo $LINKS',
      output: [
        `github   <a href="${links.github}">@Wenjia1215</a>`,
        `linkedin <a href="${links.linkedin}">wenjia wang</a>`,
        `scholar  <a href="${links.scholar}">google scholar</a>`,
        `youtube  <a href="${links.youtube}">WenjiaCybersecurity</a>`,
        `cv       <a href="${links.cv}">download pdf</a>`,
        `email    <a href="${links.email}">wenjiabusiness@gmail.com</a>`,
      ],
    },
    {
      command: '',
      muted: true,
      output: [
        'try typing: help, about, research, teaching, work, links, contact, cv, clear',
        'llm chat mode is planned. this version uses fast local replies.',
      ],
    },
  ];

  const replies = {
    help: [
      'commands: about · research · teaching · skills · work · links · contact · cv · face · clear',
      'future command: chat --llm, once the site has a hosted model endpoint.',
    ],
    about: [
      'wenjia is a cs ph.d. candidate focused on trustworthy ai, cybersecurity compliance, and cs education.',
      'the short version: i make technical systems easier to verify, explain, and teach.',
    ],
    research: [
      'research focus: verifiable ai for compliance question answering.',
      'keywords: citation grounding, retrieval evidence, answer contracts, runtime verification.',
      '<a href="publications.html">open publications</a>',
    ],
    teaching: [
      'teaching focus: programming, ai applications, cybersecurity, software engineering, data structures.',
      'service: fiu senior capstone mentor; fiu capstone showcase judge from fall 2021 to present.',
    ],
    skills: [
      'ai: rag workflows, evidence selection, grounded qa, evaluation, llm applications.',
      'security: compliance frameworks, zero trust, cloud security, policy-aware systems.',
      'teaching: project-based cs, debugging, system explanation, student mentoring.',
    ],
    work: [
      'selected work: ComplianceGPT, Zero Trust migration, cybersecurity compliance survey, Baby-Feed web app.',
      'also: FIU capstone mentoring and showcase judging across spring, summer, and fall.',
    ],
    links: [
      `github   <a href="${links.github}">@Wenjia1215</a>`,
      `linkedin <a href="${links.linkedin}">wenjia wang</a>`,
      `scholar  <a href="${links.scholar}">google scholar</a>`,
      `youtube  <a href="${links.youtube}">WenjiaCybersecurity</a>`,
    ],
    contact: [
      `email <a href="${links.email}">wenjiabusiness@gmail.com</a>`,
      'location: miami, fl',
    ],
    cv: [
      `<a href="${links.cv}">download cv pdf</a>`,
      'note: the web cv is being compressed into this terminal version.',
    ],
    face: [
      'portrait renderer: sampling pixels from assets/img/teaching-bg.png into ascii.',
      'send a clean headshot later and this gets much sharper.',
    ],
  };

  function delay(ms) {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }

  function createBlock(command = '', muted = false) {
    const block = document.createElement('div');
    block.className = 'command-block';
    if (command) {
      const line = document.createElement('div');
      line.className = 'cmd-line';
      line.innerHTML = `<span class="prompt">~$</span>${escapeHtml(command)}`;
      block.append(line);
    } else if (muted) {
      block.classList.add('system-note');
    }
    terminalLog.append(block);
    return block;
  }

  function appendOutput(block, line, muted = false) {
    const out = document.createElement('div');
    out.className = `output-line${muted ? ' muted' : ''}`;
    out.innerHTML = line;
    block.append(out);
  }

  function escapeHtml(value) {
    return value
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  async function bootTerminal() {
    terminalInput.disabled = true;
    for (const entry of bootSequence) {
      const block = createBlock(entry.command, entry.muted);
      await delay(entry.command ? 95 : 60);
      for (const line of entry.output) {
        appendOutput(block, line, entry.muted);
        await delay(34);
      }
    }
    terminalInput.disabled = false;
    terminalInput.focus({ preventScroll: true });
  }

  function normalizeCommand(value) {
    return value.trim().toLowerCase().replace(/\s+/g, ' ');
  }

  function handleCommand(rawCommand) {
    const command = normalizeCommand(rawCommand);
    if (!command) return;

    if (command === 'clear') {
      terminalLog.textContent = '';
      return;
    }

    const aliases = {
      '?': 'help',
      ls: 'work',
      'ls skills': 'skills',
      'ls skills/': 'skills',
      'ls work': 'work',
      'ls work/': 'work',
      'cat about.txt': 'about',
      'cat teaching.txt': 'teaching',
      'cat research.txt': 'research',
      'echo $links': 'links',
      whoami: 'about',
      email: 'contact',
    };

    const key = aliases[command] || command;
    const block = createBlock(rawCommand);
    const output = replies[key] || [
      `command not found: ${escapeHtml(rawCommand)}`,
      'try `help` for available commands.',
    ];
    output.forEach((line) => appendOutput(block, line));
    terminalLog.scrollTop = terminalLog.scrollHeight;
  }

  function setupTerminalInput() {
    terminalForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const value = terminalInput.value;
      terminalInput.value = '';
      handleCommand(value);
    });

    document.addEventListener('keydown', (event) => {
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      if (document.activeElement === terminalInput) return;
      if (event.key.length === 1 || event.key === '/') {
        terminalInput.focus();
      }
    });
  }

  function renderNumberRain() {
    const count = 84;
    const fragment = document.createDocumentFragment();
    for (let index = 0; index < count; index += 1) {
      const span = document.createElement('span');
      span.textContent = Math.random() > 0.5 ? '1' : '0';
      span.style.left = `${Math.random() * 100}%`;
      span.style.animationDuration = `${7 + Math.random() * 11}s`;
      span.style.animationDelay = `${Math.random() * -14}s`;
      span.style.opacity = `${0.18 + Math.random() * 0.46}`;
      fragment.append(span);
    }
    numberRain.append(fragment);
  }

  function renderAsciiPortrait() {
    const context = canvas.getContext('2d', { willReadFrequently: true });
    const image = new Image();
    image.onload = () => {
      const columns = window.innerWidth < 720 ? 72 : 92;
      const rows = window.innerWidth < 720 ? 62 : 72;
      canvas.width = columns;
      canvas.height = rows;

      const crop = {
        x: image.width * 0.56,
        y: image.height * 0.17,
        width: image.width * 0.36,
        height: image.height * 0.72,
      };

      context.drawImage(image, crop.x, crop.y, crop.width, crop.height, 0, 0, columns, rows);
      const pixels = context.getImageData(0, 0, columns, rows).data;
      const chars = ' .,:;i1tfLCG08@';
      const lines = [];

      for (let y = 0; y < rows; y += 1) {
        let line = '';
        for (let x = 0; x < columns; x += 1) {
          const offset = (y * columns + x) * 4;
          const red = pixels[offset];
          const green = pixels[offset + 1];
          const blue = pixels[offset + 2];
          const luminance = 0.299 * red + 0.587 * green + 0.114 * blue;
          const contrast = Math.max(red, green, blue) - Math.min(red, green, blue);
          const darkness = 255 - luminance + contrast * 0.42;
          const charIndex = Math.max(0, Math.min(chars.length - 1, Math.floor((darkness / 255) * chars.length)));
          line += chars[charIndex];
        }
        lines.push(line.replace(/\s+$/g, ''));
      }
      asciiFace.textContent = lines.join('\n');
    };
    image.onerror = () => {
      asciiFace.textContent = 'portrait source missing\nsend a clean headshot for the next render';
    };
    image.src = 'assets/img/teaching-bg.png';
  }

  renderNumberRain();
  renderAsciiPortrait();
  setupTerminalInput();
  bootTerminal();
})();
