import { Flex, Spacer, Button, Box } from "@chakra-ui/react";
import { FaRegCompass, FaInfoCircle, FaTree } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

function Navbar() {
  let navigate = useNavigate();

  const routeHome = () => {
    navigate("/");
  };

  const routeExplore = () => {
    navigate("/recommend");
  };

  const routeFeed = () => {
    navigate("/feed");
  };

  return (
    <Box color="gray.100" m={4} mb="12">
      <Flex>
        <Button
          leftIcon={<FaTree />}
          size="lg"
          variant="ghost"
          fontWeight="bold"
        >
          Connectify
        </Button>

        <Spacer />
        <Button
          leftIcon={<FaRegCompass />}
          size="lg"
          variant="ghost"
          fontWeight="bold"
          onClick={routeExplore}
        >
          Explore Music
        </Button>
        <Button
          leftIcon={<FaInfoCircle />}
          size="lg"
          variant="ghost"
          fontWeight="bold"
          onClick={routeFeed}
        >
          Feed
        </Button>
      </Flex>
    </Box>
  );
}

export default Navbar;
