const express = require('express');
const cors = require('cors');
const ytdl = require('ytdl-core');
const ytsr = require('ytsr');

const app = express();
app.use(cors());

app.get('/api/search', async (req, res) => {
  const query = req.query.query;
  if (!query) return res.status(400).json({ error: 'Missing query parameter' });

  try {
    // YouTube search
    const filters = await ytsr.getFilters(query);
    const videoFilter = filters.get('Type').get('Video');
    const searchResults = await ytsr(videoFilter.url, { limit: 1 });

    const firstVideo = searchResults.items[0];
    if (!firstVideo || !firstVideo.url) {
      return res.status(404).json({ error: 'No results found' });
    }

    const audioInfo = await ytdl.getInfo(firstVideo.url);
    const audioFormat = ytdl.chooseFormat(audioInfo.formats, { quality: 'highestaudio' });

    res.json({
      title: firstVideo.title,
      channel: firstVideo.author.name,
      thumbnail: firstVideo.bestThumbnail.url,
      audio_url: audioFormat.url,
      source_url: firstVideo.url,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Something went wrong', details: err.message });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
