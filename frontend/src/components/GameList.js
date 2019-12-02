import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

import styled from 'styled-components';
import Card from '@material-ui/core/Card';
import Avatar from '@material-ui/core/Avatar';
import CardContent from '@material-ui/core/CardContent';

// hack, backend's IP should be allocated dynamically 
const API_URL = "http://157.230.79.213:5000/api/v1/games?date="

const StyledCard = styled(Card)`
  background: linear-gradient(45deg, #fe6b8b 30%, #ff8e53 90%);
  border-radius: 3px;
  border: 1;
  color: white;
  width: 50%;
  margin: auto;
  margin-top: 70px;
  height: 250px;
  padding: 0 30px;
  box-shadow: 0 3px 5px 2px rgba(255, 105, 135, 0.3);
`;

function useDataFetcher() {
  const date = useSelector(state => state.dateReducer)
  const [games, setGames] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState(null);
    useEffect(() => {
      setIsLoading(true)
      setErrors(null)
      fetch(API_URL + date.date)
        .then(res => {
          if (res.ok) {
            return res.json()
          } else {
            throw Error("error fetching games")
          }
        })
        .then(games => {
          setGames(games);
          setIsLoading(false)
        })
        .catch(error => setErrors(error))
      }, [date])
    return { games, isLoading, errors }
  }
  
  
export default function GamesList() {
  
    const { games, isLoading, errors } = useDataFetcher();
    
    if (errors) {
      return <p style={{ color: "red" }}> {errors.message} </p>
    }
    if (isLoading) {
      return <p>Loading posts</p>
    }
    return (
      <div>
        {games.map(game => (
          <>
            <StyledCard>
                <CardContent>
                <Avatar alt="Remy Sharp" src="https://a1.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/scoreboard/den.png&h=70&w=70" />
                <p>{game.home_team} : {game.away_team}</p>
                <p>{game.home_score} : {game.away_score}</p>
                {/* {console.log(game.quarter_scores)} */}
                {/* <p>{game.quarter_scores.quarter_count}</p>
                <p>{game.quarter_scores.away_team_score}</p>
                <p>{game.quarter_scores.away_team_score}</p> */}
                </CardContent>
            </StyledCard>

          </>
        ))}
      </div>  
    );
};


