import { useEffect, useState } from "react";
import QrReader from "react-qr-reader";


interface AppProps {
  datasender: any;
}

const Scanner: React.FC<AppProps> = ({ datasender }) => {
  const [result, setResult] = useState("");
  const [error, setError] = useState(null);

  if (error) {
    return <div className="error">{error}</div>;
  }
  useEffect(() => {
    datasender(result);
  }, [result]);

  return (
    <div>
      <QrReader
        delay={300}
        onError={(error) => {
          setError(error.message);
        }}
        onScan={(data) => {
          if (data) {
            setResult(data);
            setError(null);
          }
        }}
        style={{ width: "100%" }}
      />
    </div>
  );
};

export default Scanner;