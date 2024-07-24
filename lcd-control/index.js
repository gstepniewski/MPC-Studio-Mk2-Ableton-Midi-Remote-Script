const express = require('express')
const midi = require('midi')
const sharp = require('sharp')

const width = 160;
const height = 80;

function intToTwoByteHex(int) {
  let hexString = int.toString(16).padStart(4, '0');
  let highByte = parseInt(hexString.slice(0, 2), 16);
  let lowByte = parseInt(hexString.slice(2, 4), 16);
  return [highByte, lowByte];
}

function magicNumber(seed) {
  function magicFormula(n) { return 128 * n - 8 }

  let n = 2
  while (magicFormula(n) <= seed) n++

  return magicFormula(n - 1)
}

function encodePng(originalBuffer) {
  const convertedBuffer = [];

  for (let i = 0; i < originalBuffer.length; i += 7) {
    const group = originalBuffer.slice(i, i + 7);
    let controlByte = 0;

    for (let j = 0; j < group.length; j++) {
      if (group[j] >= 128) {
        controlByte |= 1 << j;
        group[j] -= 128;
      }
    }

    convertedBuffer.push(controlByte, ...group);
  }

  return Buffer.from(convertedBuffer);
}

function generateMessageMetadata(x, y, decodedLength, encodedLength) {
  const imageCoordinates = [x, 0x00, y, 0x00];

  const messageLength = encodedLength + 16

  const magic = magicNumber(encodedLength);
  const meta1Dec = messageLength + magic
  const meta1 = intToTwoByteHex(meta1Dec)

  let meta2 = [0x00, 0x20]
  let meta3 = intToTwoByteHex(decodedLength).toReversed()

  if (meta3[0] >= 128) {
    meta2 = [0x20, 0x20]
    meta3 = intToTwoByteHex(decodedLength - 128).toReversed()
  }

  return [
    ...meta1,
    ...meta2,
    ...imageCoordinates,
    ...meta3,
  ];
}

function generateMessage(imageData, x, y) {
  const messageHeader = [0xf0, 0x47, 0x7f, 0x4a, 0x04];
  const encoded = encodePng(imageData)
  const messageMetadata = generateMessageMetadata(x, y, imageData.length, encoded.length)
  const terminator = [0xf7]

  return [
    ...messageHeader,
    ...messageMetadata,
    ...encoded,
    ...terminator
  ]
}

async function generateImage(title, subtitle) {
  const image = sharp({
    create: {
      width: width,
      height: height,
      channels: 3,
      background: { r: 0, g: 0, b: 0 },
    },
  });

  if (subtitle) {
    image.composite([
      {
        input: Buffer.from(`<svg width="${width}" height="${height}" viewBox="0 0 ${height} ${height}"><text x="50%" y="0%" text-anchor="middle" dy="1.2em" font-weight="bold" font-size="1.5em" fill="#fff" font-family="sans-serif" >${title}</text></svg>`),
        top: 0,
        left: 0,
      },
      {
        input: Buffer.from(`<svg width="${width}" height="${height}" viewBox="0 0 ${height} ${height}"><text x="50%" y="100%" text-anchor="middle" dy="-1em" font-size="1.5em" fill="#fff" font-family="sans-serif">${subtitle}</text></svg>`),
        top: 0,
        left: 0,
      }
    ]);
  } else {
    image.composite([{
      input: Buffer.from(`<svg width="${width}" height="${height}" viewBox="0 0 ${height} ${height}"><text x="50%" y="50%" text-anchor="middle" dy="0.4em" font-size="2em" fill="#fff" font-family="sans-serif">${title}</text></svg>`),
      top: 0,
      left: 0,
    }])
  }

  return await image.toFormat("png").toBuffer();
}

function splitImage(image) {
  const splitCoordinates = [
    [0, 0, 60, 60],
    [0, 60, 60, 20],
    [60, 0, 60, 60],
    [60, 60, 60, 20],
    [120, 0, 40, 60],
    [120, 60, 40, 20],
  ];

  return Promise.all(
    splitCoordinates.map(async (splitCoordinate, i) => {
      const [left, top, width, height] = splitCoordinate;
      const splitImage = sharp(image).extract({ left, top, width, height });
      return await splitImage
        .toFormat("png", {
          compressionLevel: 9,
          colours: 8,
        }).toBuffer()
    })
  );
}

function sendChunks(output, port, chunks) {
  output.openPort(port)
  output.sendMessage(generateMessage(chunks[0], 0, 0))
  output.sendMessage(generateMessage(chunks[1], 0, 60))
  output.sendMessage(generateMessage(chunks[2], 60, 0))
  output.sendMessage(generateMessage(chunks[3], 60, 60))
  output.sendMessage(generateMessage(chunks[4], 120, 0))
  output.sendMessage(generateMessage(chunks[5], 120, 60))
  output.closePort()
}

async function process(big, small) {
  let port = 0
  for (let i = 0; i < output.getPortCount(); i++) {
    let portName = output.getPortName(i)
    if (portName.includes('MPC Studio')) {
      port = i
      break
    }
  }

  // console.log(output.getPortName(port), big, small)

  const image = await generateImage(big, small)
  const imageChunks = await splitImage(image)
  sendChunks(output, port, imageChunks)
}

function sanitize(text) {
  return text.replaceAll("&", "&amp;")
}

// --- START ---

const app = express()
const output = new midi.Output()

app.use(express.json())

app.post('/', (req, res) => {
  res.sendStatus(200)
  let big = sanitize(req.body.big)
  let small = sanitize(req.body.small)
  process(big, small)
})

app.listen(6727)
