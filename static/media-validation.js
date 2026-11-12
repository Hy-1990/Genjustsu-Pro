"use strict";
const MediaValidation = Object.freeze({
  fileError(file, role) {
    if (!file || !file.size) return 'empty_file';
    const extension = file.name.split('.').pop().toLowerCase();
    const image = ['png', 'jpg', 'jpeg', 'webp'].includes(extension);
    const video = ['mp4', 'mov', 'webm'].includes(extension);
    if (role === 'source' ? !video : role === 'second' ? !image : !image && !video) return 'format_' + role;
    if (file.size > (role === 'source' ? 500_000_000 : 100_000_000)) return 'size_' + role;
    return null;
  },
  durationError(seconds, role, sourceSeconds = 0) {
    if (!Number.isFinite(seconds) || seconds <= 0) return 'invalid_video';
    if (seconds < (role === 'source' ? 4 : 2) || seconds > 30) return 'duration_' + role;
    if (role !== 'source' && sourceSeconds + seconds > 30) return 'reference_duration';
    return null;
  },
});
