interface Props {

    loading: boolean;

    onClick(): void;

}

export function DownloadButton({

    loading,

    onClick,

}: Props) {

    return (

        <button

            disabled={loading}

            onClick={onClick}

        >

            {

                loading

                    ? "Загрузка..."

                    : "Скачать данные"

            }

        </button>

    );

}