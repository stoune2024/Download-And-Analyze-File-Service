const [progress, setProgress] =
    useState<DownloadProgress>();

useDownloadEvents(
    setProgress,
);

<DownloadProgress
    progress={progress}
/>