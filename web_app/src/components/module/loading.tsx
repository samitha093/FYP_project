import { Spinner } from '@chakra-ui/react';

function Loading({ visible = true }) {
  if (!visible) {
    return null; // Return null to hide the component when not visible
  }
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(255, 255, 255, 0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 999 }}>
      <div style={{ textAlign: 'center' }}>
      <Spinner
            thickness='4px'
            speed='0.65s'
            emptyColor='gray.200'
            color='blue.500'
            size='xl'
            />
        <h1>Loading...</h1>
      </div>
    </div>
  );
}

export default Loading;

//for execution

// const [loadingVisible, setLoadingVisible] = useState(false);

// // Function to show the loading component
// const showLoading = () => {
//   setLoadingVisible(true);
// };

// // Function to hide the loading component
// const hideLoading = () => {
//   setLoadingVisible(false);
// };