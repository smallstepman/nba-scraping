import React from 'react';
import { MuiPickersUtilsProvider, KeyboardDatePicker } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import { useSelector, useDispatch } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import { Grid } from '@material-ui/core';


import AppBar from '@material-ui/core/AppBar';

const today = new Date(Date.now()).toISOString().slice(0,10)

export function dateReducer(state = { date: today }, action) {
      switch (action.type) {
          case "CHANGE_DATE":
              return { 
                ...state, 
                date: action.payload 
              }
              default:
                  return state;
              }
          }

const useStyles = makeStyles(theme => ({
    root: {
        height: 150,
    },
    font: {
        color: "white",
        borderBottom: "1px solid rgba(255, 255, 255, 1)"
    }
    }));



export default function DatePicker() {
    const date = useSelector(state => state.dateReducer)
    const dispatch = useDispatch()
    
    const classes = useStyles();

  
    function changeDate(value) {
      dispatch({
        type: "CHANGE_DATE",
        payload: value.toISOString().slice(0,10)
      })
    }
    
    return (
      <>
        <AppBar className={classes.root} position="sticky">
            <Grid className={classes.root}
                container
                alignContent="center"
                spacing={2}
                align="center"
                justify="center"
            >
                <Grid item>
                    
                    <MuiPickersUtilsProvider utils={DateFnsUtils}>
                        <KeyboardDatePicker
                            InputProps={{ className: classes.font }}
                            className={classes.font}
                            variant="inline"
                            format="dd MMM yyyy"
                            margin="normal"
                            id="date-picker"
                            value={date.date}
                            onChange={changeDate}
                            KeyboardButtonProps={{
                                'aria-label': 'change date',
                            }}
                        />
                    </MuiPickersUtilsProvider>
                </Grid>
            </Grid>
        </AppBar>   
      </>
    )
  }
