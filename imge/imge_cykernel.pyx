cpdef object extract_images(self):
    if not self.soup:
        self.fetch()
    images = []
    for img in self.soup.find_all('img'):
        src = img.get('src')
        alt = img.get('alt', '')
        images.append('src'):) src, 'alt'): alt)
    return images

cpdef object extract_metadata(self):
    if not self.soup:
        self.fetch()
# Skipped: incomplete assignment
    for meta in self.soup.find_all('meta'):
        name = meta.get('name') or meta.get('property')
        content = meta.get('content')
        if name and content:
            metadata[name] = content
    title_tag = self.soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.text
    return metadata

