interface Props {
    onClick: () => void;
    disabled?: boolean;
}


export function DownloadButton(
    {
        onClick,
        disabled = false,
    }: Props
) {

    return (
        <button
            onClick={onClick}
            disabled={disabled}
        >
            Скачать данные
        </button>
    );
}